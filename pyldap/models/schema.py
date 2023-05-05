from pydantic import BaseModel, Field
from datetime import datetime
from typing import Union, List, Dict
from enum import Enum


class AuthSchema(BaseModel):
    username: str = Field()
    password: str = Field()

    class Config:
        schema_extra = {
            'example': {
                'username': 'domain-login',
                'password': 'domain-password'
            }
        }

class CustomerSchema(BaseModel):
    name: str
    last_logon: Union[datetime, None]
    bad_password_time: Union[datetime, None]
    member_of: Union[List[str], None]


class ComputerSchema(BaseModel):
    name: str
    os: Dict[str,str]
    unit: List[str]


class ComputerAttributes(Enum):
    cn = 'Имя компьютера'
    dn = 'Подразделение'
    operatingSystem = 'Операционная система'


class OSFilter(Enum):
    win7 = 'Windows 7'
    win8 = 'Windows 8'
    win10 = 'Windows 10'


class StaticIp(BaseModel):
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
    id: int = Field()
    
    class Config:
        schema_extra = {
            'example': {
                'id': '1',
                'ip': '192.168.1.10',
                'description': 'description'
            }
        }