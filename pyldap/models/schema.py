from pydantic import BaseModel
from datetime import datetime
from typing import Union, List, Dict
from enum import Enum


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
    