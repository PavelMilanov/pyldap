import subprocess
import re
from typing import List

from .import cache


def generate_computer_list_from_unit_free(unit: str) -> List[str]:
    """Возвращает список пользователей в конкретном лесу.

    Args:
        unit (str): название подразделения.

    Returns:
        List[str]: список пользователей.
    """    
    data = cache.get_set_items(unit)
    return data
