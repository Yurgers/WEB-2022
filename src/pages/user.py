from fastapi import Depends, APIRouter, HTTPException

from ..schemas.user import Login, PublicUser
from ..services.user import service_init, UserServices

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
    responses={400: {"description": "Bad Request"},
               409: {"description": "Нарушена Уникальность данных"}
               },
)


@router.get("/", response_model=list[PublicUser])
def get_users(
        service: UserServices = Depends(service_init),
        # current_user: User = Depends(get_current_user)
):
    """Показывает список пользователей"""
    return service.get_many_all()


@router.get("/logins", response_model=list[Login])
def get_examples(
        service: UserServices = Depends(service_init)
):
    """Показывает список логинов"""
    return service.get_many_all()


@router.get("/{username}", response_model=PublicUser)
def get_user_by_username(username: str,
                         service: UserServices = Depends(service_init)
                         ):
    """Показывает информацю о пользователе по username"""

    return service.get_user_by_username(username)
