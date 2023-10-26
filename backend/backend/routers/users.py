from fastapi import APIRouter, Path, Security, Response
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict
import re
from tortoise.exceptions import DoesNotExist

from db.postgres.models import Act
from .auth import token_auth_scheme
from models.ldap import CustomerLdapDescribe
from .import ldap, cache


router = APIRouter(
    prefix='/api/v1/ldap3/users',
    tags=['Users']
)

@router.get('/')
async def get_customers_and_computers(
    skip: int = 0,
    limit: int = 20,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> List:
    """_Вывод сортированный список всех записей AD с атрибутами CustomerLdapDescribe.

    Args:
        skip (int, optional): Начальный индекс списка пользователей. Defaults to None.
        limit (int, optional): Конечный индекс списка пользователей. Defaults to None.
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации.

    Returns:
        List: _description_
    """    
    users = cache.get_json_set('customers', skip=skip, limit=limit)
    if users is None:  # если в кеше не окажется данных, взять из AD.
        users = ldap.get_domain_users(skip, limit)
    computers = cache.get_json_set('computers', skip=skip, limit=limit)
    if computers is None:  # если в кеше не окажется данных, взять из AD.
        computers = ldap.get_domain_computers(skip, limit)
    resp = []
    for user, computer in zip(users, computers):
        resp.append(CustomerLdapDescribe(
            name=user.name,
            description=user.description,
            member_of=user.member_of,
            os=computer.os,
            version_os=computer.version_os,
            unit=computer.unit,
            ip=''
        ))
    return resp

@router.get('/all')
async def get_customers(
    response: Response,
    skip: int = 0,
    limit: int = 20,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> List | None:
    """Вывод сортированный список всех пользователей AD с атрибутами CustomerLdap.

        Args:
            skip (int, optional): Начальный индекс списка пользователей. Defaults to None.
            limit (int, optional): Конечный индекс списка пользователей. Defaults to None.
            token (HTTPAuthorizationCredentials, optional): Токен аутентификации.

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
    customer: str = Path(description='Имя компьютера', example='customer'),  # noqa: E501
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
    # если запрос на акт не от AD.
    pattern = re.search(r"customer[0-9]{4}", customer)
    if pattern:   
        resp = await ldap.get_customer_desctibe(customer)
        return resp
    else:
        # если не пользователь AD вернуть только акт.
        return {'act': response.headers['X-Customer-Act']}

@router.get('/{customer}')
async def get_customer(
    customer: str = Path(description='Имя компьютера', example='customer', regex='customer[0-9]{4}'),  # noqa: E501
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
