from pydantic import BaseModel, Field, UUID4
from typing import List


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
    """Модель загружаемого файла(акта) пользователя."""    
    id: UUID4 = Field()
    customer: str = Field()
    file: str = Field(alias='file_name')


class NetworkClietnConfig(BaseModel):
    """Модель конфигурации клиента AD, полученной через службу NetClient v1."""    
    network: List[str] = Field()
    system: str = Field()
    time: str = Field()

    class Config:
        schema_extra = {
            'example': {
                'network': [
                        'enp2s0 1500 169.254.114.16/16 4c:52:62:3a:6a:2f',
                        'enx3c18a0064bd0 1500 155.4.13.57/23 3c:18:a0:06:4b:d0',
                        'virbr0 1500 192.168.122.1/24 52:54:00:11:7d:1c',
                ],
                'system': 'ubuntu',
                'time': '2023-07-26 17:06'
                }
        }


class NetworkClientMessage(BaseModel):
    system: str = Field()
    message: str = Field()
    time: str = Field()
    
    class Config:
        schema_extra = {
            'example': {
                "system": "iMac-pavel-milanov.local",
                "message": "login",
                'time': '2023-07-26 17:06'
            }
        }
