from fastapi import APIRouter, Security, Response
from fastapi.security import HTTPAuthorizationCredentials
from .auth import token_auth_scheme
from .import ldap


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
async def get_organizations_tree(response: Response):
    resp = await ldap.search_organizations_tree()
    count = await ldap.get_count_organizations()
    response.headers['x-unit-count'] = str(count)
    return resp

# @router.get('/count')
# async def get_count_organizations():
#     resp = await ldap.get_count_organizations()
#     return resp
