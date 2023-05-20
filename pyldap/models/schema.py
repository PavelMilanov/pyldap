from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union, List, Dict
from enum import Enum


class AuthSchema(BaseModel):
    """Модель для авторизации.

    Args:
        BaseModel (_type_): Pydantic объект.
    """    
    username: str = Field()
    password: str = Field()

    class Config:
        schema_extra = {
            'example': {
                'username': 'domain-login',
                'password': 'domain-password'
            }
        }

# class CustomerSchema(BaseModel):
#     name: str
#     last_logon: Union[datetime, None]
#     member_of: Union[List[str], None]


# class ComputerSchema(BaseModel):
#     name: str
#     os: Dict[str,str]
#     unit: List[str]


class StaticIp(BaseModel):
    """Модель для валидации данных при работе с таблицей StaticIp по REST API.

    Args:
        BaseModel (_type_): Pydantic объект.
    """    
    ip: str = Field()
    description: str = Field()
    
    class Config:
        schema_extra = {
            'example': {
                'ip': '192.168.1.10',
                'description': 'description'
            }
        }


class GetStaticIp(StaticIp):
    """Модель для получения записи из таблицы StaticIp по REST API.

    Args:
        StaticIp (_type_): _description_
    """    
    id: int = Field()
    
    class Config:
        schema_extra = {
            'example': {
                'id': '1',
                'ip': '192.168.1.10',
                'description': 'description'
            }
        }
