from apscheduler.schedulers.background import BackgroundScheduler
from .connector import Ldap3Connector
from .utilits import get_ip_address
from .import cache
from loguru import logger


ldap = Ldap3Connector()
background = BackgroundScheduler()

@background.scheduled_job('cron', hour=23)
def scheduled_nslookup_for_customer():
    logger.info('run dns polling for customers')
    data = ldap.get_computers()
    for item in data:
        computer = item.split(',')[0][3:].lower()
        customer, ip = get_ip_address(computer) 
        cache.set_value(customer, ip)

@background.scheduled_job('cron', hour='0')
def scheduled_parse_computer_for_unit():
    logger.info('run add computer for unit')
    data = ldap.get_computers()
    for item in data:
        customer = computer.entry_dn.split(',')[0][3:].lower()
        unit = computer.entry_dn.split(',')[1:-4]  # CN=CUSTOMER0003,OU=_,OU=_
    # if len(unit) == 1:
    #     unit = unit[0][3:]  # unit
    #     dn[unit] = customer
    # elif len(unit) > 1:
    #     format_unit = ''
    #     for item in unit:
    #         format_unit += item[3:] + '-'  # subunit-unit
    #         dn[format_unit[:-1]] = customer
    #     print(customer, format_unit[:-1])