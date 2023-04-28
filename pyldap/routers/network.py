from fastapi import APIRouter, Path, Query, Depends
from db.postgres.models import StaticIp
from .auth import ldap_auth


router = APIRouter(
    prefix='/api/v1/network',
    tags=['Network']
)

@router.get('/{ip}')
#async def set_static_ip(token: str = Depends(ldap_auth)):
async def get_static_ip(ip: str):
    tmp = await StaticIp.get(ip=ip)
    print(tmp.all())
    # return new_ips

@router.post('/ip')
#async def set_static_ip(token: str = Depends(ldap_auth)):
async def set_static_ip(
    ip: str = Query(description='ip address', example='127.0.0.1', regex='\d.\d.\d.\d'),
    description: str = Query(description='description'),
):
    new_ips = await StaticIp.create(ip=ip, description=description)
    return new_ips
