from datetime import datetime, timedelta, UTC
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

# Configuration
import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Not used unless explicitly passed
DEFAULT_TOKEN_EXPIRATION_DAYS = 7

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class TokenData(BaseModel):
    username: str | None = None
    user_id: str | None = None



    
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    print(data.items)
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=7))
    to_encode.update({"exp": expire})
    if "sub" not in to_encode:
        raise ValueError("The 'sub' field (username) must be included in the data.")
    print(f"Access token expiration: {expire}")  # Debugging
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




def refresh_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a refreshed JWT access token.
    Defaults to 35 days if no expires_delta is provided.
    """
    to_encode = data.copy()
    
    # Default to 35 days expiration for refresh tokens
    expire = datetime.now(UTC) + (expires_delta or timedelta(days=35))
    to_encode.update({"exp": expire})
    
    # Ensure the "sub" claim (subject) is included
    if "sub" not in to_encode:
        raise ValueError("The 'sub' field (username) must be included in the data.")
    
    # Debugging expiration
    print(f"Creating refresh token with expiration: {expire} UTC")
    
    # Encode the token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt














ACCESS_TOKEN_EXPIRES_IN = timedelta(minutes=7)
REFRESH_TOKEN_EXPIRES_IN = timedelta(days=30)
expire_time = datetime.now(UTC) + ACCESS_TOKEN_EXPIRES_IN

from jose import jwt, JWTError, ExpiredSignatureError

def verify_token(response: Response, token: str, refreshToken: str = None):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Access token payload: {payload}")
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return TokenData(user_id=user_id)

    except ExpiredSignatureError:
        print("Access token expired.")
        if refreshToken:
            try:
                payload = jwt.decode(refreshToken, SECRET_KEY, algorithms=[ALGORITHM])
                user_id: str = payload.get("sub")
                if user_id is None:
                    raise credentials_exception

                access_token = create_access_token({"sub": str(user_id)}, expires_delta=ACCESS_TOKEN_EXPIRES_IN)
                refresh_token = refresh_access_token({"sub": str(user_id)}, expires_delta=REFRESH_TOKEN_EXPIRES_IN)
                
                response.set_cookie("access_token", access_token, secure=True, samesite="lax", httponly=True)
                response.set_cookie("refresh_token", refresh_token, secure=True, samesite="lax", httponly=True)

                return TokenData(user_id=user_id)
            except JWTError as e:
                print(f"Refresh token invalid: {str(e)}")
                raise credentials_exception
        else:
            raise credentials_exception

    except JWTError as e:
        print(f"Token verification error (not expired): {str(e)}")
        raise credentials_exception
