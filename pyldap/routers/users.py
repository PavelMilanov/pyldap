from fastapi import APIRouter, Depends
from utils.connector import domain
from typing import List, Dict
# from .auth import ldap_auth


router = APIRouter(
    prefix='/api/v1/ldap3/users',
    tags=['Users']
)


@router.get('/users')
async def get_customers() -> List:
    """Вывод сортированный список всех пользователей AD с атрибутами CustomerLdap.

    Returns:
        List: Список CustomerLdap сущностей.
    """    
    resp = await domain.get_domain_users()
    return [customer for customer in resp]

@router.get('/count')
async def get_users_count() -> int:
    resp = await domain.get_count_users()  # вывод количества всех пользователей
    return resp

@router.get('/{customer}')
async def get_customer_info(
        customer: str,
        # token: str = Depends(ldap_auth)
    ) -> Dict | None:
    """Возвращает полную информацию о пользователе домена.

    Args:
        customer (str): имя customer.

    Returns:
        Dict | None: модель CustomerLdapDescribe.
    """    
    resp = await domain.get_customer_desctibe(customer)
    return resp

@router.delete('/{user}')
async def delete_user_by_name(
        user: str,
        # token: str = Depends(ldap_auth)
    ):
    resp = await domain.delete_user(name=user)
    return resp
