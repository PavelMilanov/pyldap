import dramatiq
from dramatiq.brokers.redis import RedisBroker
from environs import Env
from utils.utilits import get_ip_address
from loguru import logger
from utils.connector import Ldap3Connector
from db.redis import RedisConnector


env = Env()
env.read_env()

broker = RedisBroker(url=f"redis://{env('REDIS_HOST')}:6379/{env('REDIS_BROKER_DB')}")
dramatiq.set_broker(broker)

ldap = Ldap3Connector()
cache = RedisConnector()


#@background.scheduled_job('cron', hour=23)
def scheduled_nslookup_for_customer():
    """Добавляет в кеш ip адреса и dns имена компьютеров в AD по расписанию."""    
    logger.info('run dns polling for customers')
    data = ldap.get_computers()
    for item in data:
        computer = item.split(',')[0][3:].lower()
        customer, ip = get_ip_address(computer) 
        cache.set_value(customer, ip)

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
    
    Периодически подключается к AD и генерирует сортированный список всех пользователей и заносит в кеш.
    
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
