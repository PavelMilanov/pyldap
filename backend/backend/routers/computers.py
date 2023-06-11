from fastapi import APIRouter, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from typing import Dict
from .auth import token_auth_scheme
from .import ldap


router = APIRouter(
    prefix='/api/v1/ldap3/computers',
    tags=['Computers']
)


@router.get('/')
async def get_computer(
        customer: str = Query(description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),
        token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
        ) -> Dict | None:
    resp = await ldap.get_domain_computer(name=customer)
    if resp is not None:
        return resp
