from prettytable import PrettyTable
from utils import from_dict_items,catch,autoincrementdict
from functools import partial
from pprint import pprint

class GetColumnMixin:
    def get_values(self):
        return [getattr(self,col.name)
                for col in self.get_columns
                ]

    @classmethod
    @property
    def get_columns(cls):
        return cls.__table__.columns



class UserMixin:

    def __init__(self,id_or_user):
        from databases import User


        self.user = id_or_user if isinstance(id_or_user,User) else User.manager.get(id_or_user)
        self.actions = autoincrementdict()
        self.pt_actions = PrettyTable(('Number','Name'))
        self.set_actions(
            ('Change name',partial(User.manager.change_username,self.user)),
            ('Change password', partial(User.manager.change_password,self.user))
        )


    def set_actions(self,*actions): #tuple[str,FunctionType]
        self.pt_actions.add_rows(
            from_dict_items(self.actions.add_many(*actions))
        )

    def get_actions(self):
        print(self.pt_actions)
        self._get_actions(self.actions)

    def _get_actions(self,actions):
        while True:
            id = input()
            if id == '':
                return

            if (action:=actions.get(id,None)) is None:
                print('Такой команды нет')
                continue

            try:
                action[1]()
            except Exception as exp:
                print('Произошла ошибка! :' + str(exp))
