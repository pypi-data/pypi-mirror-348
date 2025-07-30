 
from sqlmodel import SQLModel, Field, Relationship, Session, select
from datetime import datetime
from typing import List, Optional
from uuid import uuid4, UUID


class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    first_name: Optional[str] = Field(default=None) 
    last_name: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None)
    profile_photo: Optional[str] = None
    email: str = Field(index= True, unique=True)
    password: Optional[str] = Field(default=None)
    bio: Optional[str] = None 
    verification_code: Optional[str] = Field(default=None)
    code_expiry: Optional[datetime] = Field(default=None)
    