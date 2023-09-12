from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from typing import Dict, List

from .auth import token_auth_scheme
from .import ldap
from utils.utilits import generate_computer_list_from_unit_free


router = APIRouter(
    prefix='/api/v1/ldap3/organizations',
    tags=['Organizations']
)

@router.get('/schema')
async def get_organizations_schema() -> Dict | None:
    """Возвращает схему всех подраздений со всеми отрибутами.

    Returns:
        Dict | None: json-всех подраздлений со всеми атрибутами | None
    """    
    resp = await ldap.search_organizations_schema()
    return resp

@router.get('/tree')
async def get_organizations_tree(
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> Dict[str, List[str]]:
    """Возвращает иерархию подраздений AD.

    Args:
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации.
        Defaults to Security(token_auth_scheme).

    Returns:
        Dict[str, List[str]]: {
            "unit": ["subunit1", "subunit2"],
            "unit2: [subunit1"]
            }
    """    
    resp = await ldap.search_organizations_tree()
    return resp

@router.get('/{unit}')
def get_computers_for_unit(
    unit: str,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> List[str]:
    """Возвращает список пользователей для конткретного подразделения AD.

    Args:
        unit (str): Название подраздления.
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации.
        Defaults to Security(token_auth_scheme).

    Returns:
        List[str]: ["user1", "user2"]
    """    
    return generate_computer_list_from_unit_free(unit.upper())
