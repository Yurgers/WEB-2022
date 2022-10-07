from pydantic import BaseModel, validator
import datetime

class BaseUser(BaseModel):
    username: str
    password: str
    name: str
    email: str
    gender: str
    birthdate: datetime.date
    is_active: bool


class UserCreate(BaseUser):
    pass


class UserUpdate(BaseUser):
    pass


class User(BaseUser):
    id: int

    class Config:
        orm_mode = True

class Login(BaseModel):
    username: str

    class Config:
        extra = 'allow'
        orm_mode = True