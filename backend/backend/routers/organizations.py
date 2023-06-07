from fastapi import APIRouter, Security, Response
from fastapi.security import HTTPAuthorizationCredentials
from .auth import token_auth_scheme
from .import ldap
from utils.utilits import generate_computer_list_from_unit_free


router = APIRouter(
    prefix='/api/v1/ldap3/organizations',
    tags=['Organizations']
)

@router.get('/schema')
async def get_organizations_schema():
    """Получение схемы всех подраздений со всеми отрибутами.

    Returns:
        _type_: _description_
    """    
    resp = await ldap.search_organizations_schema()
    return resp

@router.get('/tree')
async def get_organizations_tree(response: Response, token: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
    resp = await ldap.search_organizations_tree()
    return resp

@router.get('/{unit}')
def get_computers_for_unit(unit: str, token: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
    return generate_computer_list_from_unit_free(unit.upper())



# @router.get('/count')
# async def get_count_organizations():
#     resp = await ldap.get_count_organizations()
#     return resp
