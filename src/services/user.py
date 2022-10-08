from fastapi import Depends, HTTPException, status

from .base_service import BaceService
from .. import models
from ..database import Session
from ..schemas.user import UserCreate, UserUpdate



def get_user_by_username(username: str) -> models.User:
    session = Session()
    user = session.query(models.User).filter(models.User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{username=} not found"
        )

    return user


class UserServices(BaceService[models.User, UserCreate, UserUpdate]):
    def get_user_by_username(self, username: str) -> models.User:
        user = self.session.query(self.model).filter(self.model.username == username).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"{username=} not found")
        return user

def service_init(servise: UserServices = Depends()):
    servise.set_model(models.User)
    return servise
