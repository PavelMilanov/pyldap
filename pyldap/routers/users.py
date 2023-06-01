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
    ) -> Dict:
    """Возвращает полную информацию о пользователе домена.

    Args:
        customer (str): имя customer.

    Returns:
        Dict: модель CustomerLdapDescribe.
    """    
    resp = await ldap.get_customer_desctibe(customer)
    if resp is not None:
        return resp
    else:
        return {
            'os': 'not found',
            'version_os': 'not found',
            'unit': [],
            'name': 'not found',
            'description': 'not found',
            'last_logon': 'not found',
            'member_of': [],
            'ip': 'not found'
        }

@router.get('/count')
async def get_users_count() -> int:
    resp = await ldap.get_count_users()  # вывод количества всех пользователей
    return resp

@router.delete('/customer')
async def delete_user_by_name(
        user: str,
        # token: str = Depends(ldap_auth)
    ):
    resp = await ldap.delete_user(name=user)
    return resp
