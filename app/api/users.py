from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.models.orm import User, Role
from app.schemas.user import UserAssignRole
from app.core.dependencies import RoleChecker, get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])
admin_only = RoleChecker(["Admin"])

@router.post("/{user_id}/assign-role")
def assign_role(user_id: int, assign_data: UserAssignRole, db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    role = db.query(Role).filter(Role.name == assign_data.role_name).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
        
    user.role_id = role.id
    db.commit()
    return {"message": f"Assigned role {role.name} to user {user.username}"}

@router.get("/{id}/roles")
def get_user_roles(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user or not user.role:
        return {"roles": []}
    return {"roles": [user.role.name]}

@router.get("/{id}/permissions")
def get_user_permissions(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    user = db.query(User).filter(User.id == id).first()
    if not user or not user.role:
        return {"permissions": []}
    return {"permissions": user.role.permissions}
