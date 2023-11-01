from fastapi import APIRouter, Path, Security, Response
from fastapi.security import HTTPAuthorizationCredentials
from typing import List, Dict
import re
from tortoise.exceptions import DoesNotExist

from db.postgres.models import Act, NetworkClient
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
    ) -> List[CustomerLdapDescribe]:
    """Вывод сортированный список всех записей AD с атрибутами CustomerLdapDescribe.

        Args:
            skip (int, optional): Начальный индекс списка пользователей. Defaults to None.
            limit (int, optional): Конечный индекс списка пользователей. Defaults to None.
            token (HTTPAuthorizationCredentials, optional): Токен аутентификации.

    Returns:
        List: List[CustomerLdapDescribe]
    """
    data = cache.get_json_set('customers', skip=skip, limit=limit)
    for user in data:
        netclient = await NetworkClient.get_or_none(system=user['name'])
        if netclient:
            strdata = netclient.network[2:-2]  ## ethernet 1500 16.254.11.1/16 4c:52:62:3a:6a:2f
            parsedata = list(strdata.split(' '))
            user['ip'] = parsedata[2]
            user['mac'] = parsedata[3]
    return data

@router.get('/all')
async def get_customers(
    response: Response,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> None:
    """Вывод количества пользователей AD.

        Args:
            token (HTTPAuthorizationCredentials, optional): Токен аутентификации.
    """
    header = cache.get_value('customers_count')
    response.headers['X-Customers-Count'] = str(header)

@router.get('/{customer}/info')
async def get_customer_info(
    response: Response,
    customer: str = Path(description='Имя компьютера', example='customer'),  # noqa: E501
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> CustomerLdapDescribe | None:
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
        resp = ldap.get_customer_desctibe(customer)
        netclient = await NetworkClient.get_or_none(system=customer)  ## ['ethernet 1500 16.254.11.1/16 4c:52:62:3a:6a:2f']
        if netclient:
            strdata = netclient.network[2:-2]  ## ethernet 1500 16.254.11.1/16 4c:52:62:3a:6a:2f
            parsedata = list(strdata.split(' '))
            resp.ip = parsedata[2]
            resp.mac = parsedata[3]
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
    resp = ldap.get_domain_user(customer)
    return resp
