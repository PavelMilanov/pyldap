import subprocess
import re
from typing import List
import aiohttp
import asyncio

from .import env, cache


def generate_computer_list_from_unit_free(unit: str) -> List[str]:
    """Возвращает список пользователей в конкретном лесу.

    Args:
        unit (str): название подразделения.

    Returns:
        List[str]: список пользователей.
    """    
    data = cache.get_set_items(unit)
    return data

async def get_ping_request(host: str) -> int:
    """GET-запрос на сервер для определения доступности клиента.

    Args:
        host (str): ip-адрес клиента.

    Returns:
        int: статус
    """    
    params = {'host': host}
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"http://{env('NETCLIENT_SERVER')}/ping", params=params, timeout=4) as resp:
                return resp.status
        except asyncio.TimeoutError:  # если клиент не ответил в течении 4 секунд - 400 ошибка.
            return 400
