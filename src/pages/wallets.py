from fastapi import Depends, APIRouter, HTTPException
from starlette import status

from .auth import get_current_user
from ..schemas.auth import TokenData
from ..schemas.user import User, UserCreate, UserUpdate, Login, PublicUser, WalletCreate
from ..services.wallets import WalletServices, service_init

router = APIRouter(
    prefix="/wallets",
    tags=["кошелек"],
    # dependencies=[Depends(get_db)],
    responses={400: {"description": "Bad Request"},
               409: {"description": "Нарушена Уникальность данных"}
               },
)


@router.post("/new", response_model=WalletCreate)
def create_wallet(
        username: TokenData,
        service: WalletServices = Depends(service_init)
):
    """Создание нового кошелька у пользователя"""

    # service.create_wallet()

    return service.create_wallet(username.username)
