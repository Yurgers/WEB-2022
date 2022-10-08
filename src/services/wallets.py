from fastapi import Depends, HTTPException, status
import requests

from .user import UserServices
from .. import models

BASE_URL = 'https://hackathon.lsp.team/hk'
REGISTRATION_BONUS = 100

class WalletServices(UserServices):

    def check_status_code(self, resp):
        # if resp.status_code >= 500:
        #     raise HTTPException(
        #         status_code=status.HTTP_404_NOT_FOUND,
        #         detail="Удаленные сервис недоступен"
        #     )
        if resp.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resp.json()
            )
        return True

    def create_wallet(self, username: str):
        current_user = self.get_user_by_username(username)

        if current_user.publicKey:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="У пользователя уже есть Кошелек"
            )

        url = BASE_URL + "/v1/wallets/new"

        resp = requests.post(url=url)
        self.check_status_code(resp)

        current_user.publicKey = resp.json()['publicKey']
        current_user.privateKey = resp.json()['privateKey']
        self.session.commit()

        self.transfers_ruble("admin", username, REGISTRATION_BONUS)

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
        self.check_status_code(resp)
        print(resp.json())

        return resp.json()

    def show_balance(self, username):
        current_user = self.get_user_by_username(username)
        self.is_publicKey(current_user.publicKey)

        url = BASE_URL + f"/v1/wallets/{current_user.publicKey}/balance"

        resp = requests.get(url=url)
        self.check_status_code(resp)
        print(resp.json())

        return resp.json()

    def transfers_ruble(self, from_username, to_username, amount: float):
        from_current_user = self.get_user_by_username(from_username)
        self.is_publicKey(from_current_user.publicKey)
        to_current_user = self.get_user_by_username(to_username)
        self.is_publicKey(to_current_user.publicKey)

        url = BASE_URL + f"/v1/transfers/ruble"

        data = {
            "fromPrivateKey": from_current_user.privateKey,
            "toPublicKey": to_current_user.publicKey,
            "amount": amount
        }

        resp = requests.post(url=url, json=data)
        self.check_status_code(resp)
        print(resp.json())

        return resp.json()

    def transfers_status(self, transactionHash):
        url = BASE_URL + f"/v1/transfers/status/{transactionHash}"
        resp = requests.get(url=url)
        self.check_status_code(resp)
        print(resp.json())

        return resp.json()


def service_init(servise: WalletServices = Depends()):
    servise.set_model(models.User)

    return servise
