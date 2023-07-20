from fastapi import APIRouter, Path, Security, Response
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict
from tortoise.exceptions import DoesNotExist

from db.postgres.models import Act
from models.schema import ActSchema
from .auth import token_auth_scheme
from .import ldap, cache


router = APIRouter(
    prefix='/api/v1/ldap3/users',
    tags=['Users']
)

@router.get('/all')
async def get_customers(
    response: Response,
    skip: int = 0,
    limit: int = 20,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> List | None:
    """Вывод сортированный список всех пользователей AD с атрибутами CustomerLdap.

    Returns:
        List: Список CustomerLdap сущностей.
    """
    header = cache.get_value('customers_count')
    response.headers['X-Customers-Count'] = str(header)
    resp = cache.get_json_set('customers', skip=skip, limit=limit)
    if resp is None:  # если в кеше не окажется данных, взять из AD.
        return ldap.get_domain_users(skip, limit)
    return resp

@router.get('/{customer}/info')
async def get_customer_info(
    response: Response,
    customer: str = Path(description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> Dict | None:
    """Возвращает полную информацию о пользователе домена.

    Args:
        customer (str): имя customer.

    Returns:
        Dict | None: модель CustomerLdapDescribe.
    """
    try:
        await Act.get(customer=customer).values()
        response.headers['X-Customer-Act'] = 'true'
    except DoesNotExist:
        response.headers['X-Customer-Act'] = 'false'
    resp = await ldap.get_customer_desctibe(customer)
    return resp

@router.get('/{customer}')
async def get_customer(
    customer: str = Path(description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> Dict | None:
    """Вывод информации о пользователе AD c атрибутами CustomerLdap.

    Args:
        customer (str): имя пользователя.

    Returns:
        Dict | None: Dict | None: модель CustomerLdap.
    """    
    resp = await ldap.get_domain_user(customer)
    return resp
