from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError
from starlette import status

from ..schemas.user import User
from ..schemas.auth import Token, TokenData, LoginData
from ..services.auth import AuthServices, service_init, get_user_is_jwt, get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация"],
    # dependencies=[Depends(get_db)],
    responses={400: {"description": "Bad Request"},
               409: {"description": "Нарушена Уникальность данных"}
               },
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(token: str = Depends(oauth2_scheme),
                     ):
    try:
        username: str = get_user_is_jwt(token)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(username=username)
    if user is None:
        raise credentials_exception

    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 service: AuthServices = Depends(service_init)
                                 ):
    '''Логин через JWT'''
    access_token = service.get_access_token(username=form_data.username, password=form_data.password)

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=TokenData)
async def login(login: LoginData,
                service: AuthServices = Depends(service_init)
                ):
    """Заглушка для логина"""

    user = service.get_user_by_username(login.username)
    if not user:
        raise credentials_exception

    return TokenData(username=login.username)


@router.post("/me", response_model=User)
def read_me(current_user: User = Depends(get_current_user)):
    """Информация о владельце токена"""
    return current_user
