from fastapi import APIRouter, Path, Query, Depends
from utils.connector import domain
from models.schema import ComputerSchema, ComputerAttributes
# from .auth import ldap_auth


router = APIRouter(
    prefix='/api/v1/ldap3/computers',
    tags=['Computers']
)


@router.get('/computer')
async def get_computer(
        computer: str = Query(default=None, description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),
        attribute: ComputerAttributes = Query(default=ComputerAttributes.cn, description='Атрибуты для поиска с фильтрами'),
        value: str = Query(default=None,),
        # token: str = Depends(ldap_auth)
        ):
    resp = await domain.get_computer(name=computer, attribute=attribute.name, attribute_value=value)
    return [ComputerSchema(
        name=computer.name,
        os=computer.os,
        unit=computer.unit
    ) for computer in resp]

@router.get('/{unit}')
async def get_computers_by_unit(
        unit: str,
        # token: str = Depends(ldap_auth)
    ):
    return "в разработке"

@router.delete('/{computer}')
async def delete_computer_by_name(
        computer: str,
        # token: str = Depends(ldap_auth)
    ):
    resp = await domain.delete_computer(name=computer)
    return resp
