from _auth import auth,register




def main():

    while True:
        print("1. Авторизоваться\n2. Зарегистрироваться")
        cmd = input()
        if cmd == "1":
            auth()
        elif cmd == "2":
            register()
        else:
            print("Нет такой команды")


if __name__ == "__main__":
    main()