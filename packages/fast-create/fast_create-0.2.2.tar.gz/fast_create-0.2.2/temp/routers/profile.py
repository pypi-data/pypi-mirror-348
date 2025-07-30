from fastapi import APIRouter, Depends
router = APIRouter()
from imports import current_auth_bearer, current_cookie_user
from schemas.userSchema import Profile

@router.get('/users/me', response_model=Profile)
def myProfile(current_user: Profile = Depends(current_cookie_user)):
    return current_user

@router.get('/users/me/oauth', response_model=Profile)
def myProfile_oauth(current_user: Profile = Depends(current_auth_bearer)):
    return current_user