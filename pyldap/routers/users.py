from fastapi import APIRouter
from utils.connector import domain


router = APIRouter(
    prefix='/api/v1/ldap3/users',
    tags=['Users']
)


@router.get('/users')
async def get_users():
    resp = await domain.search_domain_users()
    return resp

@router.get('/{user}')
async def get_user_by_name(user: str):
    return "в разработке"

@router.get('/{unit}')
async def get_users_by_unit(unit: str):  # поиск всех пользователей в указанном подразделении
    return "в разработке"

@router.post('/{user}')
async def add_user_by_name(user: str):  # добавление компьютера вручную
    return "в разработке"

@router.delete('/{user}')
async def delete_user_by_name(user: str):
    return "в разработке"