from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from jose import jwt
from typing import Final
from .import env, cache
from datetime import date
from loguru import logger


class Authentification(HTTPBearer):
    """Основной класс для реализации авторизации/аутентификации.

    Args:
        HTTPBearer (_type_): FastApi класc.
    """    
    
    pwd_schema = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM: Final = env('ALGORITHM')
    SECRET: Final = env('SECRET')
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> None:
        """Основной метод авторизации.

        Args:
            request (Request): request.

        Raises:
            HTTPException: Ошибка авторизации.
        """        
        token = await super().__call__(request)
        logger.info(token)
        if token.scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Invalid authentication credentials',
                )
        else:
            await self.__check_token(token.credentials)

    async def generate_token(self, username: str, password: str) -> str:
        """Генерирует токен аутентификации при корректном вводе логина и пароля.

        Args:
            username (str): логин.
            password (str): пароль.

        Returns:
            str: токен.
        """        
        expired_date = await self.__expired_date()
        token = jwt.encode({'expired_date': str(expired_date)}, self.SECRET, algorithm=self.ALGORITHM)
        cache.set_value('token', token)
        return token

    async def __check_token(self, token: str) -> None:
        """Проверяет валидность токена.

        Args:
            token (str): токен аутентификации.
        """       
        cache_token = cache.get_value('token')
        try:
            decod_token = jwt.decode(token, self.SECRET, algorithms=self.ALGORITHM)
            if date.fromisoformat(decod_token['expired_date']) < date.today():
                logger.warning('Token is not valid')
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Credentials not found',
                )
                cache.delete_value('token')
            else:
                logger.success('Token is valid')
        except jwt.JWTError as e:
            logger.warning(e)
            raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Invalid token',
                )

    async def __expired_date(self) -> date:
        """Устанавливает срок жизни токена.
        По-умолчанию: 1 сутки.

        Returns:
            date: Дата окончания валидности токена.
        """        
        current_date = date.today()
        return date(current_date.year, current_date.month, current_date.day+1)
