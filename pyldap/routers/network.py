from fastapi import APIRouter, Path, Query, Depends
from db.postgres.models import StaticIp
from models import schema
from .auth import ldap_auth
from tortoise.exceptions import DoesNotExist
from typing import List


router = APIRouter(
    prefix='/api/v1/network',
    tags=['Network']
)

@router.get('/')
#async def set_static_ip(token: str = Depends(ldap_auth)):
async def get_static_ip_all() -> List[schema.GetStaticIp]:
    try:
        resp = await StaticIp.all().values()
        return [schema.GetStaticIp(**item) for item in resp]
    except DoesNotExist as e:
        print(e)

@router.post('/')
#async def set_static_ip(token: str = Depends(ldap_auth)):
async def set_static_ip(item: schema.StaticIp):
    new_item = await StaticIp.create(ip=item.ip, description=item.description)
    return new_item



@router.get('/{id}')
#async def set_static_ip(token: str = Depends(ldap_auth)):
async def get_static_ip(id: int) -> schema.GetStaticIp:
    try:
        resp = await StaticIp.get(id=id).values()
        return schema.GetStaticIp(**resp)
    except DoesNotExist as e:
        print(e)

@router.put('/{id}')
async def change_static_ip(id: int, item: schema.StaticIp):
    try:
        resp = await StaticIp.get(id=id)
        resp.update_from_dict(item.dict())
        await resp.save()
    except DoesNotExist as e:
        print(e)

@router.delete('/{id}')
async def delete_static_ip(id: int) -> bool:
    await StaticIp.get(id=id).delete()
    return True