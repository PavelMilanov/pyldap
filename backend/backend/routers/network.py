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
async def get_static_ip_all(
    token: HTTPAuthorizationCredentials = Security(token_auth_scheme)
    ) -> List[schema.GetStaticIp]:
    """Возвращает список табличных данных.
    Args:
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации.
        Defaults to Security(token_auth_scheme).

    Returns:
        List[schema.GetStaticIp]: db.postgres.StaticIp.
    """    
    try:
        resp = await StaticIp.all().values()
        return [schema.GetStaticIp(**item) for item in resp]
    except DoesNotExist as e:
        logger.exception(e)
    except TypeError:  # пустой список
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
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации.
        Defaults to Security(token_auth_scheme).
    """    
    try:
        await StaticIp.create(ip=item.ip, description=item.description)
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
        token (HTTPAuthorizationCredentials, optional): Токен аутентификации.
        Defaults to Security(token_auth_scheme).

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
async def netclient_config(config: schema.NetworkClietnConfig) -> None:
    """Принимает конфигурацию хоста AD, с помощью службы Netclient v1.
    Добавляет\обновляет данные в БД.

    Args:
        config (schema.NetworkClietnConfig): json-данные.
    """    
    try:
        resp = await NetworkClient.get_or_none(system=config.system)
        if resp is None:
            await NetworkClient.create(
                network=config.network,
                system=config.system,
                time=config.time
                )
        else:
            resp.update_from_dict(config.dict())
    except Exception as e:
        logger.exception(e)
        
@router.post('/netclient/message')
async def netclient_messages(data: schema.NetworkClientMessage) -> None:
    """Принимает системные сообщения от хостов службы Netclient v1.
    Добавляет все сообщения в кеш.
    
    Args:
        data (schema.NetworkClientMessage): json-данные.
    """    
    cache.append_json_set('messages', {
        'client': data.system,
        'message': data.message,
        'time': data.time}
        )

@router.get('/netclient/messages')
async def get_messages_log() -> List[dict]:
    # список сообщений от клиентов службы Netclient.
    data = cache.get_json_set('messages')[0]
    return data

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
        token (HTTPAuthorizationCredentials, optional):
        Defaults to Security(token_auth_scheme).
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
        token (HTTPAuthorizationCredentials, optional):
        Defaults to Security(token_auth_scheme).
    """    
    await StaticIp.get(id=id).delete()
