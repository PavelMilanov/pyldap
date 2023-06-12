from pydantic import BaseModel, validator
from datetime import datetime
from typing import Union, List
from enum import Enum


class CustomerLdap(BaseModel):
    """Модель пользователя домена."""    
    name: str
    description: str
    last_logon: Union[str, None]
    member_of: Union[List[str], None]
    
    @validator('last_logon')
    def formated_datetime(cls, data):
        if data is not None and data.find('1601') == -1:  # 1601-01-01 00:00:00+00:00 - хз откуда такая дата
            return datetime.strptime(data.split('.')[0], '%Y-%m-%d %H:%M:%S')  # '2017-10-09 12:05:39'
        else:
            return 'не авторизован'

    @validator('member_of')
    def formated_member_of(cls, data):
        if data is not None:
            return [group.split(',')[0][3:] for group in data]  # CN=Administrators -> Administrators
        else:
            return []


class OrganizationLdap(BaseModel):
    """Модель подразделения домена."""    
    name: str
    created_at: Union[str, None] # "2017-01-27 13:26:52+00:00"
    changed_at: str
    dn: str

    @validator('created_at', 'changed_at')
    def formated_datetime(cls, data):
        if data is not None:
            return datetime.strptime(data, '%Y-%m-%d %H:%M:%S%z')


class ComputerLdap(BaseModel):
    """Модель компьютера домена."""    
    os: str
    version_os: str
    unit: Union[str, None]
    
    @validator('unit')
    def formated_unit(cls, data):
        if data is not None:
            format_value = data.split(',')[1:-4]
            return data.split(',')[1:-4]


class CustomerLdapDescribe(CustomerLdap,ComputerLdap):
    """Подробная модель пользователя домена.
    Совмещает атрибуты пользователя и компьютера.

    Args:
        CustomerLdap (_type_): модель пользователя домена.
        ComputerLdap (_type_): модуль компьютера домена.
    """    
    last_logon: Union[datetime, str]
    unit: List[str]
    ip: str
    
    @validator('last_logon')
    def formated_datetime(cls, data):
        return data

    @validator('member_of', 'unit')
    def formated_member_of_and_unit(cls, data):
        if data is not None:
            return data
        else:
            return []

    @validator('unit')
    def formated_unit(cls, data):
        if data is not None:
            return data
