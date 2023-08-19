from fastapi import APIRouter, Security
from fastapi.security import HTTPAuthorizationCredentials
from tortoise.exceptions import DoesNotExist
from typing import List
from loguru import logger

from models import schema
from db.postgres.models import StaticIp, NetworkClient
from .auth import token_auth_scheme
from .import cache


router = APIRouter(
    prefix='/api/v1/network',
    tags=['Network']
)

@router.get('/')
async def get_static_ip_all(token: HTTPAuthorizationCredentials = Security(token_auth_scheme)) -> List[schema.GetStaticIp]:
    """Возвращает список табличных данных.
    Args:
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации. Defaults to Security(token_auth_scheme).

    Returns:
        List[schema.GetStaticIp]: db.postgres.StaticIp.
    """    
    try:
        resp = await StaticIp.all().values()
        return [schema.GetStaticIp(**item) for item in resp]
    except DoesNotExist as e:
        logger.exception(e)
    except TypeError as e:  # пустой список
        return []

@router.post('/')
async def set_static_ip(
    item: schema.StaticIp,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ):
    """Добавляет запись в таблицу StaticIp.

    Args:
        item (schema.StaticIp): {
            ip: str,
            description: str
        }
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации. Defaults to Security(token_auth_scheme).
    """    
    try:
        new_item = await StaticIp.create(ip=item.ip, description=item.description)
    except Exception as e:
        logger.exception(e)
        
@router.get('/{id}')
async def get_static_ip(
    id: int,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> schema.GetStaticIp:
    """Возвращает таблицу StaticIp в виде списка.

    Args:
        id (int): Возвращает запись из таблицы StaticIp по id.
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации. Defaults to Security(token_auth_scheme).

    Returns:
        schema.GetStaticIp: {
            id: str,
            description: str
        }
    """    
    try:
        resp = await StaticIp.get(id=id).values()
        return schema.GetStaticIp(**resp)
    except DoesNotExist as e:
        logger.exception(e)

@router.post('/netclient')
async def get_netclient_config(config: schema.NetworkClietnConfig):
    """Принимает конфигурацию клиента AD, с помощью службы Netclient v1.
    Добавляет\обновляет данные в БД.

    Args:
        config (schema.NetworkClietnConfig): 
    """    
    try:
        resp = await NetworkClient.get_or_none(system=config.system)
        if resp is None:
            await NetworkClient.create(network=config.network, system=config.system, time=config.time)
        else:
            resp.update_from_dict(config.dict())
        # cache.append_json_set('logon', {'client': config.system, 'time': config.time})
    except Exception as e:
        logger.exception(e)
        
@router.post('/netclient/messages')
async def get_netclient_messages(message: schema.NetworkClientMessage):
    return message

@router.put('/{id}')
async def change_static_ip(
    id: int, item: schema.StaticIp,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ):
    """Обновлеяет запись из таблицы StaticIp по id.

    Args:
        id (int): id записи.
        item (schema.StaticIp): {
            ip: str,
            description: str
        }
        token (HTTPAuthorizationCredentials, optional): _description_. Defaults to Security(token_auth_scheme).
    """    
    try:
        resp = await StaticIp.get(id=id)
        resp.update_from_dict(item.dict())
        await resp.save()
    except DoesNotExist as e:
        logger.exception(e)

@router.delete('/{id}')
async def delete_static_ip(
    id: int,
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ):
    """Удаляет запись из таблицы StaticIp по id.

    Args:
        id (int): id записи.
        token (HTTPAuthorizationCredentials, optional): _description_. Defaults to Security(token_auth_scheme).
    """    
    await StaticIp.get(id=id).delete()
