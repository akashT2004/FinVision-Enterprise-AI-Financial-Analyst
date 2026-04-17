from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.database import get_db
from app.models.orm import Role, User
from app.schemas.user import RoleCreate, Role as RoleSchema
from app.core.dependencies import RoleChecker

router = APIRouter(prefix="/roles", tags=["roles"])
admin_only = RoleChecker(["Admin"])

@router.post("/create", response_model=RoleSchema)
def create_role(role: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(admin_only)):
    db_role = db.query(Role).filter(Role.name == role.name).first()
    if db_role:
        raise HTTPException(status_code=400, detail="Role already exists")
    
    new_role = Role(name=role.name, permissions=role.permissions)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role
