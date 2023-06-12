from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Union, List, Dict
from enum import Enum


class AuthSchema(BaseModel):
    """Модель для авторизации."""    
    username: str = Field()
    password: str = Field()

    class Config:
        schema_extra = {
            'example': {
                'username': 'domain-login',
                'password': 'domain-password'
            }
        }

class StaticIp(BaseModel):
    """Модель для валидации данных при работе с таблицей StaticIp по REST API."""    
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
    """Модель для получения записи из таблицы StaticIp по REST API."""    
    id: int = Field()
    
    class Config:
        schema_extra = {
            'example': {
                'id': '1',
                'ip': '192.168.1.10',
                'description': 'description'
            }
        }


class ActSchema(BaseModel):
    id: UUID4 = Field()
    customer: str = Field()
    file: str = Field(alias='file_name')
