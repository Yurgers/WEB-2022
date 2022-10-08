from fastapi import Depends, HTTPException, status
import requests

from .user import UserServices
from .. import models

BASE_URL = 'https://hackathon.lsp.team/hk'
REGISTRATION_BONUS = 100


class WalletServices(UserServices):

    def __check_status_code(self, resp):
        if resp.status_code >= 400:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resp.json()
            )
        return True

    def __get_faucet(self):
        '''
        https://faucet.polygon.technology/

        address  : "0x613ae79ff968bc1535de711fac6fc23e44754696"
        network : "mumbai"
        rcToken : "03AIIukzh7cX0NvuPHzuRcn_suXX7B1e02e9AaoRUYNs2oIcjneg_-46HNnH63ziwQ31CcRONDgvd0gshkY-NTO_bLUySBm-3F4jC4dMi2WShPbQU0ytzNoAO3QIEc_09XgEtlrenVs9wNKFuozpgxJGwM7RmG7FPVAm42xrWiOjC2Oo1cy50DfmI1gsMIquNvmbvcsC5QDI-gDVpfF2YHESIvtkli7_4TnJyHLzXEx7qbLZc0OKORnp1ng-v07WUaihYptuwR4KmaonXkfVcmMKaiJDzvYrSK6hnXaLK1E9zYSdYOUxfZVjo3-Vva9fczDnuN2ZbfjWojR27PDD-bXBE4-1-4mtjqLh49EcQX6fjM7V-g4y9JhzG1a6qTgfJLS7v7BuVW5iiYPQL0qb29js5644hBjKaLabCuAAVqH0ZNp4j2mVn4X4rHsd3sOF_bDoNUzWThuqW3xjVnu94764HRYhOed-tbYCbGaXNb-z4-WeMIT68xeVq8man6EHUolX6m5KINr-rdH8U9NPZKdTodu5h225PLzw"
        token:"maticToken"
        '''

        data = {
            "address": "0x613ae79ff968bc1535de711fac6fc23e44754696",
            "network": "mumbai",
            "rcToken": "03AIIukzh7cX0NvuPHzuRcn_suXX7B1e02e9AaoRUYNs2oIcjneg_-46HNnH63ziwQ31CcRONDgvd0gshkY-NTO_bLUySBm-3F4jC4dMi2WShPbQU0ytzNoAO3QIEc_09XgEtlrenVs9wNKFuozpgxJGwM7RmG7FPVAm42xrWiOjC2Oo1cy50DfmI1gsMIquNvmbvcsC5QDI-gDVpfF2YHESIvtkli7_4TnJyHLzXEx7qbLZc0OKORnp1ng-v07WUaihYptuwR4KmaonXkfVcmMKaiJDzvYrSK6hnXaLK1E9zYSdYOUxfZVjo3-Vva9fczDnuN2ZbfjWojR27PDD-bXBE4-1-4mtjqLh49EcQX6fjM7V-g4y9JhzG1a6qTgfJLS7v7BuVW5iiYPQL0qb29js5644hBjKaLabCuAAVqH0ZNp4j2mVn4X4rHsd3sOF_bDoNUzWThuqW3xjVnu94764HRYhOed-tbYCbGaXNb-z4-WeMIT68xeVq8man6EHUolX6m5KINr-rdH8U9NPZKdTodu5h225PLzw",
            "token": "maticToken"
        }


    def __is_publicKey(self, publicKey):
        if not publicKey:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="У пользователя еще нет Кошелека"
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
        self.__check_status_code(resp)

        current_user.publicKey = resp.json()['publicKey']
        current_user.privateKey = resp.json()['privateKey']
        self.session.commit()

        self.transfers_ruble("admin", username, REGISTRATION_BONUS)

        return resp.json()

    def show_balance_nft(self, username):
        current_user = self.get_user_by_username(username)
        self.__is_publicKey(current_user.publicKey)

        url = BASE_URL + f"/v1/wallets/{current_user.publicKey}/nft/balance/"

        resp = requests.get(url=url)
        self.__check_status_code(resp)
        print(resp.json())

        return resp.json()

    def show_balance(self, username):
        current_user = self.get_user_by_username(username)
        self.__is_publicKey(current_user.publicKey)

        url = BASE_URL + f"/v1/wallets/{current_user.publicKey}/balance"

        resp = requests.get(url=url)
        self.__check_status_code(resp)
        print(resp.json())

        return resp.json()

    def transfers_matic(self, from_username, to_username, amount: float):
        url = BASE_URL + f"/v1/transfers/matic"

        return self.__transfers_coin(from_username, to_username, amount, url)

    def transfers_ruble(self, from_username, to_username, amount: float):
        url = BASE_URL + f"/v1/transfers/ruble"

        return self.__transfers_coin(from_username, to_username, amount, url)

    def __transfers_coin(self, from_username, to_username, amount: float, url: str):
        from_current_user = self.get_user_by_username(from_username)
        to_current_user = self.get_user_by_username(to_username)
        self.__is_publicKey(from_current_user.publicKey)
        self.__is_publicKey(to_current_user.publicKey)

        data = {
            "fromPrivateKey": from_current_user.privateKey,
            "toPublicKey": to_current_user.publicKey,
            "amount": amount
        }

        resp = requests.post(url=url, json=data)
        self.__check_status_code(resp)
        print(resp.json())

        return resp.json()

    def transfers_nft(self, from_username, to_username, tokenId: int ):
        url = BASE_URL + '/v1/transfers/nft'

        from_current_user = self.get_user_by_username(from_username)
        to_current_user = self.get_user_by_username(to_username)
        self.__is_publicKey(from_current_user.publicKey)
        self.__is_publicKey(to_current_user.publicKey)

        data = {
            "fromPrivateKey": from_current_user.privateKey,
            "toPublicKey": to_current_user.publicKey,
            "tokenId": tokenId
        }

        resp = requests.post(url=url, json=data)
        self.__check_status_code(resp)
        print(resp.json())

        return resp.json()

    def transfers_status(self, transactionHash):
        url = BASE_URL + f"/v1/transfers/status/{transactionHash}"
        resp = requests.get(url=url)
        self.__check_status_code(resp)
        print(resp.json())

        return resp.json()


def service_init(servise: WalletServices = Depends()):
    servise.set_model(models.User)

    return servise
