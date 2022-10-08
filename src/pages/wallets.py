from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from .auth import get_current_user
from ..schemas.auth import TokenData
from ..schemas.wallets import  Wallet, WalletBalance, WalletBalanceNFT
from ..services.wallets import WalletServices, service_init

router = APIRouter(
    prefix="/wallets",
    tags=["кошелек"],
    # dependencies=[Depends(get_db)],
    responses={400: {"description": "Bad Request"},
               409: {"description": "Нарушена Уникальность данных"}
               },
)


@router.post("/new", response_model=Wallet)
def create_wallet(
        username: TokenData,
        service: WalletServices = Depends(service_init)
):
    """Создание нового кошелька у пользователя"""

    # service.create_wallet()

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