from pydantic import BaseModel, validator
import datetime

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class LoginData(BaseModel):
    username: str
    password: str | None = None
