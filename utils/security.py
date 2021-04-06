from datetime import datetime, timedelta
from time import time
from fastapi.exceptions import HTTPException

import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
from starlette import status

oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")

from models.jwt_user import JWTUser
from utils.const import JWT_ALGORITHM, JWT_EXPIRATION_TIME_MINUTES, JWT_SECREY_KEY

pwd_context = CryptContext(schemes=["bcrypt"])

jwt_user1 = {
    "username": "user1",
    "password": "$2b$12$zltl2zvF74cX/MNMsjDEweRLrh3CwfFOYy9CwYHCnioMBZLHPiR3W",
    "disabled": False,
    "role": "ADMIN",
}
fake_jwt_user1 = JWTUser(**jwt_user1)


def get_hashed_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False


# Authenticate username and password to give JWT token
def authenticate_user(user: JWTUser):
    if fake_jwt_user1.username == user.username:
        if verify_password(user.password, fake_jwt_user1.password):
            user.role = "ADMIN"
            return user

    return None


# Create access JWT Token
def create_jwt_token(user: JWTUser):
    expiration_date = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    expiration = datetime.timestamp(expiration_date)
    print(expiration)
    jwt_payload = {"sub": user.username, "expiration": expiration, "role": user.role}
    jwt_token = jwt.encode(jwt_payload, JWT_SECREY_KEY, algorithm=JWT_ALGORITHM)
    return jwt_token


# Check whether JWT is correct
# the token provided here is given by the oauth_schema which checks the header
def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token, JWT_SECREY_KEY, algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("expiration")
        now_timestamp = datetime.timestamp(datetime.utcnow())
        if now_timestamp < expiration:
            if fake_jwt_user1.username == username:
                return final_checks(role)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    # check role and other things
    if role == "ADMIN":
        return True

    return False