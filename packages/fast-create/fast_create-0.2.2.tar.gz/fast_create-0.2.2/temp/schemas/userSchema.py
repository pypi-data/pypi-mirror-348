from typing import Optional
from pydantic import BaseModel

class Profile(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    is_online: Optional[bool] = False
    is_verified: Optional[bool] = False
    email: Optional[str] = None
    bio: Optional[str] = None