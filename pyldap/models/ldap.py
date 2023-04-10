from pydantic import BaseModel, validator
from datetime import datetime
from typing import Union, List
from enum import Enum


class CustomerLdap(BaseModel):
    name: str
    last_logon: Union[str, None]
    bad_password_time: Union[str, None]
    member_of: Union[List[str], None]
    
    @validator('last_logon', 'bad_password_time')
    def formated_datetime(cls, data):
        if data is not None and data.find('1601') == -1:  # 1601-01-01 00:00:00+00:00 - хз откуда такая дата
            return datetime.strptime(data.split('.')[0], '%Y-%m-%d %H:%M:%S')  # '2017-10-09 12:05:39'

    @validator('member_of')
    def formated_member_of(cls, data):
        if data is not None:
            return [group.split(',')[0][3:] for group in data]  # CN=Administrators -> Administrators


class OrganizationLdap(BaseModel):
    name: str
    created_at: Union[str, None] # "2017-01-27 13:26:52+00:00"
    changed_at: str
    dn: str

    @validator('created_at', 'changed_at')
    def formated_datetime(cls, data):
        if data is not None:
            return datetime.strptime(data, '%Y-%m-%d %H:%M:%S%z')


class ResponseLdap(BaseModel):
    description: str
    resp_type: str


class ComputerLdapOS(BaseModel):
    name: str
    version: str
    

class ComputerLdap(BaseModel):
    name: str
    os: ComputerLdapOS
    unit: Union[str, None]
    
    @validator('unit')
    def formated_unit(cls, data):
        if data is not None:
            format_value = data.split(',')[1:-4]
            return data.split(',')[1:-4]
