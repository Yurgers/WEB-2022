from pydantic import BaseModel, validator
import datetime

class BaseWallet(BaseModel):
    pass


class WalletCreate(BaseModel):
    privateKey: str
    publicKey: str


class WalletUpdate(BaseWallet):
    pass


class Wallet(BaseWallet):


    class Config:
        extra = 'allow'
        orm_mode = True

