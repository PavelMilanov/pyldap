from datetime import date
import calendar


def expired_date(year, month, day):
        """Моделирует метод __expired_date класса backend.utils.auth.Authentification"""
        current_date = date(year, month, day)     
        last_day = calendar.monthrange(current_date.year, current_date.month)[1]
        if current_date.day == last_day:
            return date(current_date.year, current_date.month+1, 5)
        else:
            return date(current_date.year, current_date.month, current_date.day+5)
            
#### tests  ####

def test_expired_date():
    assert expired_date(2023, 5, 31) == date(2023, 6, 5)
    assert expired_date(2023, 5, 4) == date(2023, 5, 9)
