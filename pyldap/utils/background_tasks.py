from apscheduler.schedulers.background import BackgroundScheduler
from .connector import Ldap3Connector
from .shell import get_ip_address
from .import cache
from loguru import logger


ldap = Ldap3Connector()
background = BackgroundScheduler()

@background.scheduled_job('cron', hour=23)
def scheduled_nslookup_for_customer():
    logger.info('run dns polling for customers')
    computers = ldap.get_computers()
    for computer in computers:
        customer, ip = get_ip_address(computer) 
        cache.set_value(customer, ip)
