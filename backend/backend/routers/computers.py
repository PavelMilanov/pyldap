from fastapi import APIRouter, Query, Security
from fastapi.security import HTTPAuthorizationCredentials
from typing import Dict, List

from .auth import token_auth_scheme
from .import ldap


router = APIRouter(
    prefix='/api/v1/ldap3/computers',
    tags=['Computers']
)

@router.get('/all')
async def  get_computers(
    skip: int = 0,
    limit: int = 20,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
) -> List | None:
    """Вывод сортированного списка всех компьютеров AD с атрибутами ComputerLdap.

    Args:
        skip (int, optional): Начальный индекс списка пользователей. Defaults to None.
        limit (int, optional): Конечный индекс списка пользователей. Defaults to None.
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации.

    Returns:
        List | None: Список ComputerLdap.
    """
    return ldap.get_domain_computers(skip, limit)

@router.get('/')
async def get_computer(
    customer: str = Query(description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),  # noqa: E501
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> Dict | None:
    """Поиск компьютера в лесу AD.

        Args:
            customer (str, optional): имя компьютера. Defaults to Query(description='Имя компьютера', example='customer', regex='customer[0-9]{4}').

    Returns:
        Dict | None: компьютер.
    """    
    resp = ldap.get_domain_computer(name=customer)
    if resp is not None:
        return resp
