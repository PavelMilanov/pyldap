from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from db.postgres.models import StaticIp
from models import schema
from .auth import token_auth_scheme
from tortoise.exceptions import DoesNotExist
from typing import List


router = APIRouter(
    prefix='/api/v1/network',
    tags=['Network']
)

@router.get('/')
async def get_static_ip_all(token: HTTPAuthorizationCredentials = Security(token_auth_scheme)) -> List[schema.GetStaticIp]:
    try:
        resp = await StaticIp.all().values()
        return [schema.GetStaticIp(**item) for item in resp]
    except DoesNotExist as e:
        print(e)
    except TypeError as e:  # пустой список
        return []

@router.post('/')
async def set_static_ip(item: schema.StaticIp, token: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
    new_item = await StaticIp.create(ip=item.ip, description=item.description)
    return new_item

@router.get('/{id}')
async def get_static_ip(id: int, token: HTTPAuthorizationCredentials = Security(token_auth_scheme)) -> schema.GetStaticIp:
    try:
        resp = await StaticIp.get(id=id).values()
        return schema.GetStaticIp(**resp)
    except DoesNotExist as e:
        print(e)

@router.put('/{id}')
async def change_static_ip(id: int, item: schema.StaticIp, token: HTTPAuthorizationCredentials = Security(token_auth_scheme)):
    try:
        resp = await StaticIp.get(id=id)
        resp.update_from_dict(item.dict())
        await resp.save()
    except DoesNotExist as e:
        print(e)

@router.delete('/{id}')
async def delete_static_ip(id: int, token: HTTPAuthorizationCredentials = Security(token_auth_scheme)) -> bool:
    await StaticIp.get(id=id).delete()
    return True
