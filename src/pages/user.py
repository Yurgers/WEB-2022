from fastapi import Depends, APIRouter, HTTPException

from .auth import get_current_user
from ..schemas.user import User, UserCreate, UserUpdate, Login
from ..services.user import service_init, UserServices

router = APIRouter(
    prefix="/user",
    tags=["Пользователи"],
    # dependencies=[Depends(get_db)],
    responses={400: {"description": "Bad Request"},
               409: {"description": "Нарушена Уникальность данных"}
               },
)


@router.get("/", response_model=list[User])
def get_examples(
        skip: int | None = None,
        limit: int | None = None,
        service: UserServices = Depends(service_init),
        current_user: User = Depends(get_current_user)
):
    """Показывает список ..."""
    return service.get_many(skip=skip, limit=limit)


@router.get("/logins", response_model=list[Login])
def get_examples(
        service: UserServices = Depends(service_init)
):
    """Показывает список ..."""
    return service.get_many_all()


@router.get("/{obj_id}", response_model=User)
def get_example(obj_id: int,
                service: UserServices = Depends(service_init)
                ):
    """Показывает информацю о ..."""
    print(service.get(obj_id).__dict__)

    return service.get(obj_id)
