from fastapi import Depends, HTTPException, status

from .base_service import BaceService
from .. import models
from ..schemas.user import UserCreate, UserUpdate


class UserServices(BaceService[models.User, UserCreate, UserUpdate]):
    pass


def service_init(servise: UserServices = Depends()):
    servise.set_model(models.User)
    return servise
