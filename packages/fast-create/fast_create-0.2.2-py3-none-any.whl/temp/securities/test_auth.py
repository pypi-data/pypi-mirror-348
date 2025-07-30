# test_auth.py
import pytest
from datetime import timedelta
from jose import jwt
from  .auth_token import  create_access_token, refresh_access_token, verify_token, SECRET_KEY, ALGORITHM, TokenData
from fastapi import Response, HTTPException

@pytest.fixture
def sample_data():
    return {"sub": "testuser"}


def test_create_access_token(sample_data):
    token = create_access_token(sample_data)
    assert isinstance(token, str)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == sample_data["sub"]
    assert "exp" in decoded

def test_refresh_access_token(sample_data):
    token = refresh_access_token(sample_data)
    assert isinstance(token, str)

    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == sample_data["sub"]
    assert "exp" in decoded

def test_verify_token_valid(sample_data):
    token = create_access_token(sample_data)
    response = Response()
    token_data = verify_token(response, token)
    assert isinstance(token_data, TokenData)
    assert token_data.user_id == sample_data["sub"]


def test_verify_token_invalid():
    invalid_token = "this.is.not.valid"
    with pytest.raises(Exception):  # HTTPException is raised in verify_token
        verify_token(invalid_token)

def test_create_access_token_missing_sub():
    with pytest.raises(ValueError):
        create_access_token({"foo": "bar"})
