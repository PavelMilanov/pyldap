from fastapi import APIRouter, Path, Query, Depends
from typing import Dict
# from .auth import ldap_auth
from .import ldap


router = APIRouter(
    prefix='/api/v1/ldap3/computers',
    tags=['Computers']
)


@router.get('/')
async def get_computer(
        # computer: str = Query(default=None, description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),
        # attribute: ComputerAttributes = Query(default=ComputerAttributes.cn, description='Атрибуты для поиска с фильтрами'),
        customer: str
        # token: str = Depends(ldap_auth)
        ) -> Dict | None:
    # resp = await domain.get_computer(name=computer, attribute=attribute.name, attribute_value=value)
    # return [ComputerSchema(
    #     name=computer.name,
    #     os=computer.os,
    #     unit=computer.unit
    # ) for computer in resp]
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
