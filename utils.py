import re
import functools
from datetime import datetime as dt

from consts import error_message

def check_password(password: str) -> bool:

    if not re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$", password) or \
            re.search("password123|qwerty123", password):
        print(error_message)
        return False
    return True

def pretty_estate(estate: tuple):
    print(f'{estate[0]}.Комнат: {estate[-2]}, {estate[1]} м^2, картинка - {estate[4]}. {"Открыто" if estate[4] else "Закрыто"}')

def pretty_ad(ads: tuple):
    print(f'{dt.fromtimestamp(ads[3]).isoformat()} - {"Открыто" if ads[4] else "Закрыто"}: Цена {ads[2]} Недвижимость - {ads[-1]}')

def catch(err_msg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except Exception as ex:
                print(err_msg,ex)
        return wrapper
    return decorator