from pydantic import BaseModel
from typing import List, Optional

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    permissions: List[str]

class Role(RoleBase):
    id: int
    permissions: List[str]

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    role_id: Optional[int] = None

    class Config:
        from_attributes = True
        
class UserAssignRole(BaseModel):
    role_name: str
