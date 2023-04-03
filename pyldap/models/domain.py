from pydantic import BaseModel, validator
from datetime import datetime
from typing import Union


class Customer(BaseModel):
    name: str
    lastlogon: datetime


class Organization(BaseModel):
    name: str
    created_at: Union[str, datetime] # "2017-01-27 13:26:52+00:00"
    changed_at: str
    dn: str

    @validator('created_at')
    def formated_created_at(cls, data):
        try:
            return datetime.strptime(data, '%Y-%m-%d %H:%M:%S%z')
        except Exception as e:
            print(e)
    
    @validator('changed_at')
    def formated_changed_at(cls, data):
        try:
            return datetime.strptime(data, '%Y-%m-%d %H:%M:%S%z')
        except Exception as e:
            print(e)


class OrganizationResponse(BaseModel):
    description: str
    resp_type: str

class Computer(BaseModel):
    name: str
