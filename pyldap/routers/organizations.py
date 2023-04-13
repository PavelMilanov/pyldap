from fastapi import APIRouter, Depends
from utils.connector import domain
from .auth import ldap_auth


router = APIRouter(
    prefix='/api/v1/ldap3/organizations',
    tags=['Organizations']
)

@router.get('/schema')
async def get_organizations_schema(token: str = Depends(ldap_auth)):
    """Получение схемы всех подраздений со всеми отрибутами.

    Returns:
        _type_: _description_
    """    
    resp = await domain.search_organizations_schema()
    return resp

@router.get('/tree')
async def get_organizations_tree(token: str = Depends(ldap_auth)):
    resp = await domain.search_organizations_tree()
    return resp

@router.get('/count')
async def get_count_organizations(token: str = Depends(ldap_auth)):
    resp = await domain.get_count_organizations()
    return resp

@router.get('/{unit}')
async def get_organization_by_name(
        unit: str,
        token: str = Depends(ldap_auth)
    ):
    resp = await domain.search_organization_by_name(name=unit)
    return resp

@router.post('/{unit}')
async def add_organization_by_name(
        unit: str,
        token: str = Depends(ldap_auth)
    ):
    resp = await domain.add_organization(name=unit)
    return resp

@router.delete('/{unit}')
async def delete_organization_by_name(
        unit: str,
        token: str = Depends(ldap_auth)
    ):
    resp = await domain.delete_organization(name=unit)
    return resp
