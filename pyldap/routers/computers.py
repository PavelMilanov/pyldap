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

# @router.get('/unit/{unit}')
# async def get_computers_by_unit(
#         unit: str,
#         # token: str = Depends(ldap_auth)
#     ):
#     return "в разработке"

# @router.get('/name/{name}')
# async def get_computer_by_name(name: str):
#     resp = await domain.get_computer(name)
#     return resp

# @router.delete('/{computer}')
# async def delete_computer_by_name(
#         computer: str,
#         # token: str = Depends(ldap_auth)
#     ):
#     resp = await domain.delete_computer(name=computer)
#     return resp

# @router.get('/test')
# def test():
#     ldap.get_computers()