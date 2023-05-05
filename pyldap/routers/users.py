from fastapi import APIRouter, Depends
from utils.connector import domain
from models.schema import CustomerSchema
from typing import List
# from .auth import ldap_auth


router = APIRouter(
    prefix='/api/v1/ldap3/users',
    tags=['Users']
)


@router.get('/users')
async def get_users() -> List[CustomerSchema]:
    resp = await domain.get_domain_users()
    return [CustomerSchema(name=customer.name,
            last_logon=customer.last_logon,
            bad_password_time=customer.bad_password_time,
            member_of=customer.member_of) for customer in resp]

@router.get('/count')
async def get_users_count() -> int:
    resp = await domain.get_count_users()  # вывод количества всех пользователей
    return resp

@router.get('/{user}')
async def get_user_by_name(
        user: str,
        # token: str = Depends(ldap_auth)
    ) -> CustomerSchema:
    resp = await domain.get_domain_user(name=user)
    if resp is not None:
        return CustomerSchema(
        name=resp.name,
        last_logon=resp.last_logon,
        bad_password_time=resp.bad_password_time,
        member_of=resp.member_of,
    )
    else:
        return 'Пользователь не найден'

@router.delete('/{user}')
async def delete_user_by_name(
        user: str,
        # token: str = Depends(ldap_auth)
    ):
    resp = await domain.delete_user(name=user)
    return resp
