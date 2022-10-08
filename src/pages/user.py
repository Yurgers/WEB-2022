from fastapi import Depends, APIRouter, HTTPException

from .auth import get_current_user
from ..schemas.user import User, UserCreate, UserUpdate, Login, PublicUser
from ..services.user import service_init, UserServices

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
    # dependencies=[Depends(get_db)],
    responses={400: {"description": "Bad Request"},
               409: {"description": "Нарушена Уникальность данных"}
               },
)


# @router.options('/')
# @router.head('/')
@router.get("/", response_model=list[PublicUser])
def get_examples(
        service: UserServices = Depends(service_init),
        # current_user: User = Depends(get_current_user)
):
    """Показывает список пользователей"""
    return service.get_many_all()


# @router.options('/logins')
# @router.head('/logins')
@router.get("/logins", response_model=list[Login])
def get_examples(
        service: UserServices = Depends(service_init)
):
    """Показывает список ..."""
    return service.get_many_all()


# @router.options('/{obj_id}')
# @router.head('/{obj_id}')
@router.get("/{username}", response_model=PublicUser)
def get_user_by_username(username: str,
                         service: UserServices = Depends(service_init)
                         ):
    """Показывает информацю о ..."""

    return service.get_user_by_username(username)
