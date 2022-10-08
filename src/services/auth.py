from datetime import datetime, timedelta
from jose import JWTError, jwt

from fastapi import Depends, HTTPException
from starlette import status

from service.password import verify_password
from src import models
from src.database import Session
from src.services.user import UserServices

# openssl rand -hex 32
SECRET_KEY = "4a7c28970f10b3a9f798647ecc91c27703615bcbdb54f1c78393cda5654773d9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60


# session = Session()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_jwt_user(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload.get("sub")


def get_user_by_username(username: str) -> models.User:
    session = Session()
    user = session.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )

    return user


class AuthServices(UserServices):
    def get_access_token(self, username: str, password: str):
        user = self.authenticate_user(username, password)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )

        return access_token

    def authenticate_user(self, username: str, password: str):
        user = self.get_user_by_username(username)

        if not user:
            return False
        if not verify_password(password, user.password):
            return False

        return user

    def get_user_by_username(self, username: str) -> models.User:
        user = self.session.query(self.model).filter(self.model.username == username).first()

        return user

    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     data={"sub": user.username}, expires_delta=access_token_expires
    # )


def service_init(servise: AuthServices = Depends()):
    servise.set_model(models.User)
    return servise
