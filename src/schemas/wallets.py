from pydantic import BaseModel, validator
import datetime



class Wallet(BaseModel):
    privateKey: str
    publicKey: str


class WalletBalance(BaseModel):
    maticAmount: float
    coinsAmount: float

class NFT(BaseModel):
    URI: str
    tokens: list[int]


class WalletBalanceNFT(BaseModel):
    balance: list[NFT]
