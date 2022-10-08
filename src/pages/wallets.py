from fastapi import Depends, APIRouter, HTTPException

from ..schemas.auth import TokenData
from ..schemas.wallets import Wallet, WalletBalance, WalletBalanceNFT, TransfersData, TransactionHash, StatusData
from ..services.wallets import WalletServices, service_init

router = APIRouter(
    prefix="/wallets",
    tags=["кошелек"],
    responses={400: {"description": "Bad Request"},
               409: {"description": "Нарушена Уникальность данных"}
               },
)


@router.post("/new", response_model=Wallet)
def create_wallet(
        username: TokenData,
        service: WalletServices = Depends(service_init)
):
    """Создание нового кошелька у пользователя
    + бонус за регистрацю
    """

    return service.create_wallet(username.username)


@router.post("/balance", response_model=WalletBalance)
def show_balance(
        username: TokenData,
        service: WalletServices = Depends(service_init)
):
    """показать баланс кошелька у пользователя"""

    return service.show_balance(username.username)


@router.post("/balance_nft", response_model=WalletBalanceNFT)
def show_balance_nft(
        username: TokenData,
        service: WalletServices = Depends(service_init)
):
    """показать баланс NFT кошелька у пользователя"""
    return service.show_balance_nft(username.username)


@router.post("/transfers/ruble", response_model=TransactionHash)
def transfers_ruble(
        data: TransfersData,
        service: WalletServices = Depends(service_init)
):
    """Сделать перевод Digital Ruble между пользователей"""
    return service.transfers_ruble(data.from_username, data.to_username, data.amount)


@router.get("/transfers/status/{transactionHash}", response_model=StatusData)
def show_transfers_status(transactionHash: str,
                          service: WalletServices = Depends(service_init)
                          ):
    """показать баланс NFT кошелька у пользователя"""
    return service.transfers_status(transactionHash)
