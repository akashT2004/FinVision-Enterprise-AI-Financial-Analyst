from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    permissions = Column(JSON, default=list) 
    
    users = relationship("User", back_populates="role")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=True)
    role = relationship("Role", back_populates="users")

class Document(Base):
    __tablename__ = "documents"

    document_id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    company_name = Column(String, index=True)
    document_type = Column(String, index=True)
    uploaded_by = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    file_path = Column(String)
