from pydantic import BaseModel, validator, ValidationError
from datetime import datetime
from typing import Union, List


class Customer(BaseModel):
    name: str
    last_logon: str
    bad_password_time: Union[str, None]
    member_of: Union[List[str], None]
    
    @validator('last_logon')
    def formated_last_logon(cls, data):
        if data is not None and data.find('1601') == -1:  # 1601-01-01 00:00:00+00:00 - хз откуда такая дата
            return datetime.strptime(data.split('.')[0][2:], '%Y-%m-%d %H:%M:%S')  # '2017-10-09 12:05:39'
        else:
            return None
        
    @validator('bad_password_time')
    def formated_bad_password_time(cls, data):
        if data is not None and data.find('1601') == -1:  # 1601-01-01 00:00:00+00:00 - хз откуда такая дата
            return datetime.strptime(data.split('.')[0][2:], '%Y-%m-%d %H:%M:%S')  # '2017-10-09 12:05:39'
        else:
            return None
    
    @validator('member_of')
    def formated_member_of(cls, data):
        if data is not None:
            for group in data:
                print(group.split(',')[0])
        else:
            return None

class Organization(BaseModel):
    name: str
    created_at: Union[str, datetime] # "2017-01-27 13:26:52+00:00"
    changed_at: str
    dn: str

    @validator('created_at')
    def formated_created_at(cls, data):
        if data is not None:
            return datetime.strptime(data, '%Y-%m-%d %H:%M:%S%z')
        else:
            return None
    
    @validator('changed_at')
    def formated_changed_at(cls, data):
        if data is not None:
            return datetime.strptime(data, '%Y-%m-%d %H:%M:%S%z')
        else:
            return None


class OrganizationResponse(BaseModel):
    description: str
    resp_type: str

class Computer(BaseModel):
    name: str
