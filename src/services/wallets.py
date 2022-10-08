from fastapi import Depends, HTTPException, status
import requests

from .user import UserServices
from .. import models

BASE_URL = 'https://hackathon.lsp.team/hk'


class WalletServices(UserServices):
    def create_wallet(self, username: str):
        current_user = self.get_user_by_username(username)

        if current_user.publicKey:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="У пользователя уже есть Кошелек"
            )

        url = BASE_URL + "/v1/wallets/new"

        resp = requests.post(url=url)

        current_user.publicKey = resp.json()['publicKey']
        current_user.privateKey = resp.json()['privateKey']
        self.session.commit()

        return resp.json()

    def is_publicKey(self, publicKey):
        if not publicKey:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="У пользователя еще нет Кошелека"
            )

        return True

    def show_balance_nft(self, username):
        current_user = self.get_user_by_username(username)
        self.is_publicKey(current_user.publicKey)

        url = BASE_URL + f"/v1/wallets/{current_user.publicKey}/nft/balance/"

        resp = requests.get(url=url)
        print(resp.json())

        return resp.json()




    def show_balance(self, username):
        current_user = self.get_user_by_username(username)
        self.is_publicKey(current_user.publicKey)

        url = BASE_URL + f"/v1/wallets/{current_user.publicKey}/balance"

        resp = requests.get(url=url)
        print(resp.json())

        return resp.json()


def service_init(servise: WalletServices = Depends()):
    servise.set_model(models.User)

    return servise
