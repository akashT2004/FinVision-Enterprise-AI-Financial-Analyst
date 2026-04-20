from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.orm import User, Role
from app.schemas.user import UserCreate, User as UserSchema
from app.schemas.auth import Token
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

def ensure_roles(db: Session):
    """Ensure basic roles exist and return the Admin role."""
    admin_role = db.query(Role).filter(Role.name == "Admin").first()
    if not admin_role:
        admin_role = Role(name="Admin")
        db.add(admin_role)
        db.add(Role(name="Analyst"))
        db.add(Role(name="Auditor"))
        db.add(Role(name="Client"))
        db.commit()
        db.refresh(admin_role)
    return admin_role

@router.post("/register", response_model=UserSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Auto-seed roles if none exist
    admin_role = ensure_roles(db)
    
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    
    # Check if this is the FIRST user. If so, make them Admin.
    is_first_user = db.query(User).count() == 0
    new_user = User(
        username=user.username, 
        hashed_password=hashed_password,
        role_id=admin_role.id if is_first_user else None
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Auto-seed roles and fix 'admin' user if they have no role
    admin_role = ensure_roles(db)
    
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # EMERGENCY FIX: If user is 'admin' and has no role, provide Admin role
    if user.username == "admin" and not user.role_id:
        user.role_id = admin_role.id
        db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
