from pydantic import BaseModel, validator


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


class TransfersData(BaseModel):
    from_username: str
    to_username: str
    amount: float


class TransactionHash(BaseModel):
    transaction: str


class StatusData(BaseModel):
    status: str
