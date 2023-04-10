from fastapi import APIRouter, Path, Query
from utils.connector import domain
from models.schema import ComputerSchema, ComputerAttributes


router = APIRouter(
    prefix='/api/v1/ldap3/computers',
    tags=['Computers']
)


# @router.get('/computers')
# async def get_computers():
#     resp = await domain.get_computer_by_attribute()
#     return resp

@router.get('/computer')
async def get_computer(
        computer: str = Query(default=None, description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),
        attribute: ComputerAttributes = Query(default=ComputerAttributes.cn, description='Атрибуты для поиска с фильтрами'),
        value: str = Query(default=None,)):
    resp = await domain.get_computer(name=computer, attribute=attribute.name, attribute_value=value)
    return [ComputerSchema(
        name=computer.name,
        os=computer.os,
        unit=computer.unit
    ) for computer in resp]

@router.get('/os')
async def get_computers_operation_systems():
    resp = await domain.get_computers_os_system()
    return resp


@router.get('/{unit}')
async def get_computers_by_unit(unit: str):  # поиск всех компов в указанном подразделении
    return "в разработке"


@router.delete('/{computer}')
async def delete_computer_by_name(computer: str):
    return "в разработке"
