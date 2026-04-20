from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from sqlalchemy.orm import Session
from .config import settings
from app.models.database import get_db
from app.models.orm import User, Role
from app.schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
        
    # SELF-HEALING: If user is 'admin' and has no role, fix it immediately
    if user.username == "admin" and not user.role:
        # Get or create Admin role
        admin_role = db.query(Role).filter(Role.name == "Admin").first()
        if not admin_role:
            admin_role = Role(name="Admin")
            db.add(admin_role)
            db.add(Role(name="Analyst"))
            db.commit()
            db.refresh(admin_role)
            
        user.role_id = admin_role.id
        db.commit()
        db.refresh(user)
        
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user

class RoleChecker:
    def __init__(self, required_roles: list[str]):
        self.required_roles = required_roles

    def __call__(self, current_user: User = Depends(get_current_active_user)):
        if not current_user.role or current_user.role.name not in self.required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
