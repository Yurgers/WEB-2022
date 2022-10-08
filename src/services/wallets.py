import json

from fastapi import Depends, HTTPException, status
import requests

from .auth import get_user_by_username
from .base_service import BaceService
from .user import UserServices
from .. import models
from ..database import Session, get_session
from ..schemas.user import UserCreate, UserUpdate, WalletCreate

BASE_URL = 'https://hackathon.lsp.team/hk'


class WalletServices(UserServices):

    def create_wallet(self, username: str):
        current_user = self.session.query(models.User).filter(models.User.username == username).first()

        if current_user.publicKey:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="У пользователя уже есть Кошелек"
            )

        url = BASE_URL + "/v1/wallets/new"

        resp = requests.post(url=url)
        print(resp.json())

        current_user.publicKey = resp.json()['publicKey']
        current_user.privateKey = resp.json()['privateKey']

        print(current_user.__dict__)

        self.session.commit()

        return resp.json()

def service_init(servise: WalletServices = Depends()):
    servise.set_model(models.User)

    return servise
