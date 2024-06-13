from connection import w3
from utils import check_password


def auth(public_key,password):
    try:
        w3.geth.personal.unlock_account(public_key, password)
        return True
    except Exception as ex:
        print(ex)
        return None


def register(password):
    try:
        if check_password(password):
            public_key = w3.geth.personal.new_account(password)
            return public_key
    except Exception as ex:
        print(ex)
        return None

