from pydantic import BaseModel, validator
from datetime import datetime
from typing import Union, List


class CustomerLdap(BaseModel):
    """Модель пользователя домена."""    
    name: str
    description: str
    member_of: Union[List[str], None]
    
    @validator('member_of')
    def formated_member_of(cls, data):
        if data is not None:
            # CN=Administrators -> Administrators
            return [group.split(',')[0][3:] for group in data]
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
    os: Union[str, None]
    version_os: Union[str, None]
    unit: Union[str, None]
    
    @validator('unit')
    def formated_unit(cls, data):
        if data is not None:
            if isinstance(data, list):
                return data
            return data.split(',')[1:-4]

class CustomerLdapDescribe(BaseModel):
    """Подробная модель пользователя домена.
    Совмещает атрибуты пользователя и компьютера.
    """
    name: str
    description: str
    member_of: Union[List[str], None]    
    os: str
    version_os: str
    unit: Union[List[str], None]
    ip: Union[str, None]
    mac: Union[str, None]
