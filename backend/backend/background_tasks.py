import dramatiq
from dramatiq.brokers.redis import RedisBroker
from environs import Env
from loguru import logger

from utils.connector import Ldap3Connector
from db.redis import RedisConnector


env = Env()
env.read_env()

broker = RedisBroker(url=f"redis://{env('REDIS_HOST')}:6379/{env('REDIS_BROKER_DB')}")
dramatiq.set_broker(broker)

ldap = Ldap3Connector()
cache = RedisConnector()


@dramatiq.actor
def scheduled_parse_computer_for_unit():
    """Фоновая задача.
    
    Периодически подключается к AD и делает список пользователей по подразделениям.
    
    Задача выполняется в будние дни с 9 до 18 каждые 3 часа.
    """    
    data = ldap.get_computers()
    for item in data:
        customer = item.split(',')[0][3:].lower()
        unit = item.split(',')[1:-4]  # CN=CUSTOMER0003,OU=_,OU=_
        format_unit = ''
        for item in unit:
            format_unit += item[3:] + '-'  # subunit-unit
            cache.add_set_item(format_unit[:-1], customer)
    logger.info('set computer for unit')

@dramatiq.actor
def scheduled_generate_customers_cache():
    """Фоновая задача.
    
    Периодически подключается к AD и генерирует сортированный список
    всех пользователей и заносит в кеш.
    
    Счетчик количеста пользователей заносится в кеш.

    Задача выполняется в будние дни с 9 до 17 каждые 2 часа.
    """    
    del_cache = cache.del_json_set('customers')  # очишаем список
    if del_cache == 1:
        logger.info('flush customers cache')
    else:
        logger.warning('failed to flush customers cache')
    data = ldap.get_domain_users()
    cache.set_value('customers_count', len(data))  # счетчик всех пользователей
    data = [item.dict() for item in data]
    set_cache = cache.set_json_set('customers', data)  # пишем заново
    if set_cache == 1:
        logger.info('set customers cache')
    else:
        logger.warning('failed to set customer cache')

@dramatiq.actor
def scheduled_clear_messages_cache():
    """Фоновая задача.
    
    По будням чистит кеш сообщений для websocket.
    
    Задача выполняется в будние дни в 0 часов.
    """    
    clear_cache = cache.clear_json_set('messages')
    if clear_cache == 1:
        logger.info('clear messages cache')
    else:
        logger.warning('failed to clear messages')
