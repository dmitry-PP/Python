from rolls import login,register
from utils import UserNotFound,ManagerNotFound



class Console:
    authorization = {
        '1':register,
        '2':login
    }

    def run(self):
        while True:
            try:
                user = self.authorization.get(input('1. Регистрация\n2. Войти\n'))()
                user.get_actions()
            except UserNotFound:
                print('Пользователь не найден')
            except ManagerNotFound:
                print('Обработчик данной роли не найден')
            except TypeError:
                print('Нет такого действия')
            except Exception as exp:
                print('Попробуйте еще раз',exp)



