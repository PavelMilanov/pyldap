from passlib.context import CryptContext
from jose import jwt
from typing import Final
from environs import Env
from datetime import date
from db.redis import cache


env = Env()
env.read_env()


class Authentification:
    
    pwd_schema = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ALGORITHM: Final = env('ALGORITHM')
    SECRET: Final = env('SECRET')
    
    
    async def generate_token(self, username: str, password: str) -> str:
        expired_date = await self.__expired_date()
        token = jwt.encode({'expired_date': str(expired_date)}, self.SECRET, algorithm=self.ALGORITHM)
        cache.set_value('token', token)
        # print(token)
        return token

    async def check_token(self, token: str) -> bool:
        """Проверяет валидность токена.

        Args:
            token (str): токен аутентификации.

        Returns:
            bool: успешная путентификация.
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
        current_date = date.today()
        return date(current_date.year, current_date.month, current_date.day+2)


auth = Authentification()
