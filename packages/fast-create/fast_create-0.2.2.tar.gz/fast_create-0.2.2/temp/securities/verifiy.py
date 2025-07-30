
from fastapi import APIRouter
import  temp.database as database
from typing import List
from fastapi import Depends, status, Response, HTTPException
from sqlmodel import Session, select 
from uuid import UUID
from oauth2 import get_current_user
import oauth2
from  hashing import Hash
from fastapi import  File, UploadFile, Response, status
get_db = database.get_db
router = APIRouter()
from fastapi.responses import FileResponse
import shutil
import os
from fastapi import UploadFile
from models.UserModel import User
import logging
logging.basicConfig(level=logging.INFO)
from fastapi import  Form
from datetime import datetime, timedelta
from app import app
import secrets


verification_code = secrets.token_hex(8)




@router.post("/send-verification-code")
def send_verification_code(email: str, db: Session = Depends(get_db)):
    # Generate a random verification code

    expiration_time = datetime.now() + timedelta(minutes=10)

    # Check if the user already exists in the database
    user = db.exec(select(User).where(User.email == email)).first()

    if not user:
        user = User(email=email)
        db.add(user)
    
    user.verification_code = verification_code
    user.code_expiry = expiration_time
    db.commit()

    # Simulate sending the code to the user's email
    return {"message": f"Verification code sent to {email}"}





@router.put('/verify-code')
def verify_code(verification_code: str, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.verification_code == verification_code)).first()

    if user:
        if user.verification_code !=verification_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid verification')
        if user.code_expiry < datetime.now():
            raise HTTPException(status_code=400, detail='sorry your code is expired')
    
        user.is_otp_verified = True
        user.verification_code = None
        user.code_expiry = None
        db.commit()
        db.refresh(user)
        return {"message": "Account verified successfully"}
    else:
        raise HTTPException(status_code=404, detail="Invalid Email sent")
    


@router.put('/forgot-password/receive-token')
def get_forgot_password_token(email: str = None, username: str =None, db: Session =Depends(get_db)):
    if email:
        user = db.exec(select(User).where(User.email == email)).first()

        user.code_expiry = datetime.now + timedelta(minutes=10)
        user.verification_code = verification_code
        db.commit()
        db.refresh(user)
        return f"password changed succesfully"

    elif username:
        user = db.exec((User).where(User.username == username)).first()
        user.code_expiry = datetime.now + timedelta(minutes=10)

        user.verification_code = verification_code
        db.commit()
        db.refresh(user)
        return f"password changed succesfully"
    

@router.put('/forgot-password/verify-token')   
def verify_forgot_password_token(token: str, email: str = None, username: str = None, db: Session = Depends(get_db)):
    if email != None:
        user = db.exec(select(User).where(User.email == email and  User.verification_code ==  token and User.code_expiry < datetime.now)).first()
        user.verification_code = None
        user.code_expiry = None
        db.commit()
        db.refresh(user)
        return f'token now verified with email: {email}, \n you can now proceed to password reset'
    
    elif username != None:
        user = db.exec(User).where(User.username == username and User.verification_code ==  token and User.code_expiry < datetime.now)).first()
        user.verification_code = None
        user.code_expiry = None
        db.commit()
        db.refresh(user)
        return f'token now verified with username {username}, \n you can now proceed to password reset'

        


@router.put('/change-password')
async def Forgot_password(password: str, username: str = None, email: str = None,   db: Session = Depends(get_db)):
    if username != None:
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"user with username {username} not found")
        user.password = Hash.bcrypt(password),
        db.commit()
        db.refresh(user)
    elif email != None:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"user with email {email} not found")
        user.password = Hash.bcrypt(password),

        db.commit()
        db.refresh(user)
    return user
       



