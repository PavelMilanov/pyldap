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
async def get_static_ip_all() -> List[schema.StaticIp]:
    try:
        resp = await StaticIp.all().values()
        return [schema.StaticIp(**item) for item in resp]
    except DoesNotExist as e:
        print(e)

@router.post('/')
#async def set_static_ip(token: str = Depends(ldap_auth)):
async def set_static_ip(item: schema.StaticIp):
    new_item = await StaticIp.create(ip=item.ip, description=item.description)
    return new_item

@router.get('/{ip}')
#async def set_static_ip(token: str = Depends(ldap_auth)):
async def get_static_ip(ip: str) -> schema.StaticIp:
    try:
        resp = await StaticIp.get(ip=ip).values()
        return schema.StaticIp(**resp)
    except DoesNotExist as e:
        print(e)


@router.delete('/{ip}')
async def delete_static_ip(ip: str) -> bool:
    await StaticIp.get(ip=ip).delete()
    return True