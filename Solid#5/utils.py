import re
from datetime import datetime as dt
import functools
from flask import flash

from consts import EstateType,Status


def check_password(password: str) -> bool:

    if not re.search(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$", password) or \
            re.search("password123|qwerty123", password):
        return False
    return True


def catch(err_msg):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args,**kwargs):
            try:
                res = func(*args,**kwargs)
                return res if not res is None else True
            except Exception as ex:
                flash(err_msg+" "+ex.__str__(),'danger')
        return wrapper
    return decorator


def get_type(estate):
    return EstateType.get(estate[-1])

def get_status_estate(estate):
    return Status.get(estate[3])

def get_status_ad(ad):
    return Status.get(ad[4])

def get_time(ad):
    return dt.fromtimestamp(ad[3]).isoformat()