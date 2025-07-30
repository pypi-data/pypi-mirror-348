from fastapi import APIRouter, Depends, BackgroundTasks
from fastapi import Depends, status, Response, HTTPException
from sqlmodel import Session, select
 
from hashing import Hash
from .tokenSchema import Token, TokenData, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm
import token
from models.UserModel import User
from datetime import datetime, timezone, timedelta
from jose import JWTError, jwt
from database import get_db
import secrets 
from fastapi_mail import FastMail, MessageSchema 
from pydantic import EmailStr
router = APIRouter()
from .import auth_token
from utilities.mail import conf 
from sqlalchemy.sql import or_
verification_code = secrets.token_hex(8)



create_access_token = auth_token.create_access_token
refresh_access_token = auth_token.refresh_access_token
SECRET_KEY = auth_token.SECRET_KEY
ALGORITHM = auth_token.ALGORITHM
ACCESS_TOKEN_EXPIRES_IN = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRES_IN = timedelta(days=30)
expire_time = datetime.utcnow() + ACCESS_TOKEN_EXPIRES_IN

@router.get('/auth/refresh/{token}')
def refresh_token(token: str, db: Session= Depends(get_db)):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="inavlid refresh token provided")
        user = db.exec(select(User).where(User.id == user_id)).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        new_access_token = auth_token.create_access_token(data={'sub': str(user.id)}, expires_delta=ACCESS_TOKEN_EXPIRES_IN)

        return RefreshToken(
            access_token=new_access_token, refresh_token=token, token_type='bearer', TimeStamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid refresh token')
        
@router.post('/login')
def login(response: Response,request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.username == request.username)).first()
    if not user or not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)}, expires_delta=ACCESS_TOKEN_EXPIRES_IN)
    refresh_token = refresh_access_token({"sub": str(user.id)}, expires_delta=REFRESH_TOKEN_EXPIRES_IN)
    expires_at = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRES_IN
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer", expires_at=expires_at)

@router.post("/logout")
def logout(response: Response):
    response.set_cookie(key="access_token", value="", httponly=True, expires=0)
    response.set_cookie(key="refresh_token", value="", httponly=True, expires=0)
    return {"message": "Logged out successfully"}

@router.post('/auth/login')
def login(request: OAuth2PasswordRequestForm = Depends(), db:Session =Depends(get_db)):
        user = db.exec(select(User).where(User.username == request.username)).first()
        if not user or not Hash.verify(user.password, request.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token({"sub": user.id}, expires_delta=ACCESS_TOKEN_EXPIRES_IN)
        refresh_token = refresh_access_token({"sub": user.id}, expires_delta=REFRESH_TOKEN_EXPIRES_IN)
        expires_at = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRES_IN

        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer", expires_at=expires_at)






@router.post("/send-email/")
async def send_email(email: EmailStr, background_tasks: BackgroundTasks):
    # Create the email message
    message = MessageSchema(
        subject="Cofoundr Email verification mail",
        recipients=[email],
        body="Thank you for registering! Please confirm your email.",
        subtype="plain"
    )

    # Send the email in the background
    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message)

    return {"message": "Email sent successfully!"}


def send_email_verification(code: str, email: EmailStr, background_tasks: BackgroundTasks):
    # Define the HTML email template
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email Verification</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #000;
                color: #fff;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                background: #129d37;
                border-radius: 8px;
                text-align: center;
            }}
            .header h1 {{
                font-size: 22px;
                margin: 10px 0;
            }}
            .content {{
                font-size: 16px;
                line-height: 1.6;
            }}
            .code-block {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 20px;
                font-weight: bold;
                background: #fff;
                color: #000;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .footer {{
                font-size: 12px;
                margin-top: 20px;
                color: #aaa;
            }}
            .footer a {{
                color: #fff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>App Email Verification</h1>
                <p>Please verify your email address to complete your registration.</p>
            </div>
            <div class="content">
                <p>Thank you for signing up! To confirm your email address, please use the verification code below:</p>
                <div class="code-block">{code}</div>
                <p>If you did not sign up for {"app name"}, please ignore this email.</p>
            </div>
            <div class="footer">
                <p>
                    This email was sent to you by Cofoundr. If you have any questions, please 
                    <a href="mailto:support@cofoundr.com">contact us</a>.
                </p>
                <p>&copy; {2025} Cofoundr. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Create the email message
    message = MessageSchema(
        subject=f"Cofoundr Email Verification - Code: {code}",
        recipients=[email],
        body=html_content,
        subtype="html"
    )

    # Send the email in the background
    fm = FastMail(conf)  # Ensure `conf` is correctly set up
    background_tasks.add_task(fm.send_message, message)

    return {"message": "Email sent successfully!"}



@router.post("/auth/signup")
def send_verification_code(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Generate a random verification code
    random_username = secrets.token_hex(4)
    verification_code = secrets.token_hex(3)

    expiration_time = datetime.now() + timedelta(minutes=10)

    # Check if the user already exists in the database
    user = db.exec(select(User).where(User.email == email)).first()
    if user:
        user.verification_code = verification_code
        user.code_expiry = expiration_time
        user.username = random_username
        db.add(user)
        db.commit()
        send_email_verification(email=email, code=verification_code, background_tasks=background_tasks)
        return {"message": f"Verification code sent to {email}"}


    new_user = User(username = random_username, email=email, verification_code=verification_code, code_expiry = expiration_time)
    db.add(new_user)
    db.commit()

    send_email_verification(email=email, code=verification_code, background_tasks=background_tasks)

    return {"message": f"Verification code sent to {email}"}





@router.put('/auth/verify-code')
def verify_code(email: str, verification_code: str, db: Session = Depends(get_db)):
    if not email or not verification_code:
        raise HTTPException(status_code=400, detail="Email and verification code are required")

    user = db.exec(select(User).where(User.verification_code == verification_code, User.email == email)).first()

    if user:
        if user.code_expiry < datetime.now():
            raise HTTPException(status_code=400, detail='sorry your code is expired')
        if user.is_otp_verified:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="This account is already verified")
        user.is_otp_verified = True
        user.verification_code = None
        user.code_expiry = None
        db.commit()
        return {"message": "Account verified successfully"}
    else:
        raise HTTPException(status_code=404, detail="Invalid Email sent")
    



@router.put('/auth/complete-signup')
def create_user(email: str, username: str, first_name: str,  last_name: str, password: str, phone_number: str,  db: Session=Depends(get_db)):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user.is_otp_verified:
            raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="This account is not yet verified verified")
    username = username.lower()
    if user:
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.profile_photo = "https://placehold.co/500x500/png"
        user.password = Hash.bcrypt(password)  
        user.phone_number = phone_number
        db.commit()
        
    else:
        raise HTTPException(status_code=404, detail="Sorry this user was not found")
    return user

 

 
@router.put('/auth/complete-signup/new')
def create_user_new(email: str, username: str, password: str, db: Session=Depends(get_db)):
    user = db.exec(select(User).where(or_(User.email == email, User.username == username))).first()

    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='sorry please use another email or username')
    username = username.lower()
    hashed_password = Hash.bcrypt(password)
    
    new_user = User(username = username, email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
        
    return new_user








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
        user = db.exec(select(User).where(User.username == username)).first()
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
        user = db.exec(select(User).where(User.username == username and User.verification_code ==  token and User.code_expiry < datetime.now)).first()
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
       



