from fastapi.security import HTTPBearer
from passlib.context import CryptContext
from jose import jwt
from typing import Final
from .import env
from datetime import date
from db.redis import cache


class Authentification(HTTPBearer):
    """Основной класс для реализации авторизации/аутентификации.

    Args:
        HTTPBearer (_type_): FastAPI класс.
    """    
    
    pwd_schema = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM: Final = env('ALGORITHM')
    SECRET: Final = env('SECRET')
    
    
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

    async def check_token(self, token: str) -> bool:
        """Проверяет валидность токена.

        Args:
            token (str): токен аутентификации.

        Returns:
            bool: статус.
        """       
        cache_token = cache.get_value('token')
        decod_token = jwt.decode(token, self.SECRET, algorithms=self.ALGORITHM)
        if date.fromisoformat(decod_token['expired_date']) < date.today():
            print('токен не валиден')
            return False
        else:
            print('токен валиден')
            return True

    async def __expired_date(self) -> date:
        """Валидация токена.

        Returns:
            date: Дата окончания валидности токена.
        """        
        current_date = date.today()
        return date(current_date.year, current_date.month, current_date.day+2)
