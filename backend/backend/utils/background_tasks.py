from apscheduler.schedulers.background import BackgroundScheduler
from .connector import Ldap3Connector
from .utilits import get_ip_address
from .import cache
from loguru import logger


job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

ldap = Ldap3Connector()
background = BackgroundScheduler(job_defaults=job_defaults)

@background.scheduled_job('cron', hour=23)
def scheduled_nslookup_for_customer():
    """Добавляет в кеш ip адреса и dns имена компьютеров в AD по расписанию."""    
    logger.info('run dns polling for customers')
    data = ldap.get_computers()
    for item in data:
        computer = item.split(',')[0][3:].lower()
        customer, ip = get_ip_address(computer) 
        cache.set_value(customer, ip)

@background.scheduled_job('cron', hour=0)
def scheduled_parse_computer_for_unit():
    """Сопоставляет подразделение домена с пользователями."""    
    logger.info('run add computer for unit')
    data = ldap.get_computers()
    for item in data:
        customer = item.split(',')[0][3:].lower()
        unit = item.split(',')[1:-4]  # CN=CUSTOMER0003,OU=_,OU=_
        format_unit = ''
        for item in unit:
            format_unit += item[3:] + '-'  # subunit-unit
            cache.add_set_item(format_unit[:-1], customer)
