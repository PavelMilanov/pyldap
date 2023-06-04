from fastapi import APIRouter, Path, Security
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict
from .auth import token_auth_scheme
from .import ldap

router = APIRouter(
    prefix='/api/v1/ldap3/users',
    tags=['Users']
)


@router.get('/')
async def get_customers(token: HTTPAuthorizationCredentials = Security(token_auth_scheme)) -> List | None:
    """Вывод сортированный список всех пользователей AD с атрибутами CustomerLdap.

    Returns:
        List: Список CustomerLdap сущностей.
    """    
    resp = await ldap.get_domain_users()
    return [customer for customer in resp]

@router.get('/{customer}')
async def get_customer_info(
        customer: str = Path(description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),
        token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> Dict | None:
    """Возвращает полную информацию о пользователе домена.

    Args:
        customer (str): имя customer.

    Returns:
        Dict | None: модель CustomerLdapDescribe.
    """    
    resp = await ldap.get_customer_desctibe(customer)
    return resp

@router.get('/count')
async def get_users_count() -> int:
    resp = await ldap.get_count_users()  # вывод количества всех пользователей
    return resp
