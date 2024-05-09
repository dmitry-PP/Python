from connection import w3
from functions import *
from consts import menu
from utils import check_password


def auth():
    public_key = input("Введите публичный ключ: ")
    password = input("Введите пароль: ")
    try:
        w3.geth.personal.unlock_account(public_key, password)
        print("Вы авторизованы")
        login_user(public_key)
    except Exception as ex:
        print("Ошибка авторизации:",ex)

def register():

    while True:
        password = input("Введите пароль: ")
        if password == "":
            return
        elif check_password(password):
            break
    try:
        public_key = w3.geth.personal.new_account(password)
        print(f"Адрес нового аккаунта: {public_key}")
        login_user(public_key)
    except Exception:
        print("Ошибка при создании аккаунта:")

def login_user(address):

    while True:
        print(menu)
        cmd = input()
        if cmd == "1":
            createEstate(address)
        elif cmd == "2":
            updateEstateStatus(address)
        elif cmd == "3":
            getEstates(address)
        elif cmd == "4":
            createAd(address)
        elif cmd == "5":
            updateAdStatus(address)
        elif cmd == "6":
            getAds(address)
        elif cmd == "7":
            buyEstate(address)
        elif cmd == "8":
            getBalance(address)
        elif cmd == "9":
            withDraw(address)
        elif cmd == "10":
            break
        else:
            print("Такого действия нет.")