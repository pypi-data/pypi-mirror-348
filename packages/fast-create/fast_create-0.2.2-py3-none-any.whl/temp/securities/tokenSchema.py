from pydantic import BaseModel
from datetime import datetime




class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_at: datetime

class RefreshToken(BaseModel):
    access_token: str
    token_type: str
    TimeStamp: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
    expires_at: str 
