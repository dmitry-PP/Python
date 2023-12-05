from databases import User,Roll,Store,History,Base,Session
from prettytable import PrettyTable
from mixins import UserMixin
from utils import autoincrementdict,from_dict_items,catch,\
    UserNotFound,ManagerNotFound,CountProductError
from functools import partial
from sqlalchemy import insert




class Client(UserMixin):


    def __init__(self,id):
        super().__init__(id)
        self.set_actions(
            ('Add becket',self.add),
            ('Remove becket',self.remove),
            ('Print becket',self.print_becket),
            ('Show products',partial(Store.manager.filter,'availability=true')),
            ('Filter products',Store.manager.filter),
            ('Order',self.order),
            ('Show history',partial(History.manager.print_user_history,self.user))
            )


        self.becket = {}
        self.pt = PrettyTable(('id','Product', 'Count'))


    def add(self):
        count,product = self._get_product()

        self.becket.setdefault(product,0)
        if product.availability:
            if product.count - count > 0:
                product.count-=count
            elif product.count - count ==0:
                product.count = 0
                product.availability=False
            else: raise CountProductError('Нет столько товара для добавления!')
            self.becket[product]+=count
            Session.commit()
            print('Добавлено в корзину')


    def remove(self):
        count,product = self._get_product()

        if from_becket:=self.becket.get(product,0):
            rest = (from_becket - count)
            if rest > 0:
                self.becket[product]-=rest
                product.count += count
            elif rest == 0:
                product.count = count
                del self.becket[product]
            else: raise CountProductError('Нет столько товара для удаления!')
            if not product.availability:
                product.availability = True
            Session.commit()
            print('Удалено из корзины')



    @staticmethod
    def _get_product():
        id_pr = int(input('Введите id товара: '))
        count = abs(int(input('Введите кол-во товара: ')))
        product: Store = Store.manager.get(id_pr)
        return count,product

    def print_becket(self):

        self.pt.add_rows(map(lambda item: (item[0].id,item[0].product_name,item[1]),self.becket.items()))
        print(self.pt)
        self.pt._rows.clear()

    def order(self):
        print('Ordered!!!')
        History.manager.insert_order(self.becket,self.user)
        self.becket.clear()


class Manager(UserMixin):
    def __init__(self, id):
        super().__init__(id)
        self.set_actions(
            ('Add product',Store.manager.insert),
            ('Filter store',Store.manager.filter),
            ('Sholl all store',Store.manager.all),
            ('Update positions',Store.manager.update),
            ('Delete positions',Store.manager.delete)
        )




class Admin(UserMixin):
    def __init__(self, id):
        super().__init__(id)
        self.set_actions(*zip(Base._Base__NAMES_TABLES.keys(),
                                   [partial(self.get_action_db,table) for table in Base._Base__NAMES_TABLES.values()]))


        self.pt_action_db = PrettyTable(('Number', 'Name'))


    def get_action_db(self,table):
        actions_db = self._setup_db_actions( table)

        self.pt_action_db.add_rows(
            from_dict_items(
                actions_db.items()
            )
        )
        print(self.pt_action_db)

        self._get_actions(actions_db)

        print(self.pt_actions)
        self.pt_action_db._rows.clear()

    def _setup_db_actions(self,table):
        name_db = table.__tablename__
        action_db = autoincrementdict()
        action_db.add_many(
            (f'Insert {name_db}',table.manager.insert),
            (f'FIlter {name_db}',table.manager.filter),
            (f'All {name_db}',table.manager.all),
            (f'Update {name_db}',table.manager.update),
            (f'Delete {name_db}',table.manager.delete)
                )
        return action_db


MANAGERS = {
    'client':Client,
    'manager':Manager,
    'admin':Admin
}

def _get_manager(user):
    if user is None:
        raise UserNotFound('Такого пользователя нет')

    manager = MANAGERS.get(user.roll.name, None)

    if manager is None:
        raise ManagerNotFound('Такого менеджера нет')

    return manager(user)

def login():
    user = Session.query(User).filter(
        User.username == input('Введите имя: '),
        User.password == input('Введите пароль: ')
    ).first()
    return _get_manager(user)

def register():
    try:
        user = Session.scalars(
            insert(User).returning(User),
            {'username':input('Введите свое имя: '),
             'password':input('Введите пароль: '),
             'roll_id':1}
        ).first()
        Session.commit()
        return _get_manager(user)
    except:
        print('Возникла ошибка с регистрацией')

