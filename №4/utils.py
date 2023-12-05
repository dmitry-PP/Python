from prettytable import PrettyTable


class autoincrementdict(dict):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.__id = 0

    def add(self,value):
        self.__id = int(self.last)+1
        self[self.last] = value
        return (self.last,value)

    def add_many(self,*args):
        tup = tuple()
        for value in args:
            tup+=(self.add(value),)
        return tup

    @property
    def last(self):
        return str(self.__id)

def from_dict_items(items):
    return list(
        map(
            lambda key: (key[0], key[1][0]), items
        ))


def catch(func):
    def wrap(*args,**kwargs):
        try:
            func(*args,**kwargs)
        except Exception as er:
            print(f'Возникла ошибка попробуйте еще раз! ({er.args})')
    return wrap


def add_manager(manager):
    def wrapper(cls):
        cls.manager = manager(cls)
        return cls
    return wrapper


class UserNotFound(Exception):
    pass

class ManagerNotFound(Exception):
    pass

class CountProductError(Exception):
    pass