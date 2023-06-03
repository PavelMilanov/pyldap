import subprocess
import re


def get_ip_address(customer: str) -> str:
    """Сопоставляет доменному имени ip адрес.

    Args:
        customer (str): доменное имя компютера.

    Returns:
        str: dns имя, ip.
    """    
    with subprocess.Popen(['nslookup', customer], stdout=subprocess.PIPE, text=True) as proc:
        result = proc.stdout.read()
        ip = result.strip().split()[-1] # ['Server:', '127.0.0.53', 'Address:', '127.0.0.53#53', 'Non-authoritative', 'answer:', 'Name:', 'customer1168.you.domain', 'Address:', '10.4.115.76']
        customer = result.strip().split()[-3].split('.')[0]
    return customer, ip
