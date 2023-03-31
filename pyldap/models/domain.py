from pydantic import BaseModel
from datetime import datetime


class Customer(BaseModel):
    name: str
    lastlogon: datetime

class Organization(BaseModel):
    name: str
    
class Computer(BaseModel):
    name: str