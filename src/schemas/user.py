from pydantic import BaseModel, validator
import datetime

class BaseUser(BaseModel):
    username: str
    name: str
    email: str | None
    gender: str | None
    birthdate: datetime.date | None
    is_active: bool
    publicKey: str | None


class UserCreate(BaseUser):
    password: str


class UserUpdate(BaseUser):
    pass


class User(BaseUser):
    id: int
    privateKey: str

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str

    class Config:
        extra = 'allow'
        orm_mode = True


class PublicUser(BaseUser):
    id: int

    class Config:
        orm_mode = True


class WalletCreate(BaseModel):
    privateKey: str
    publicKey: str