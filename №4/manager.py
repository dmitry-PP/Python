from sqlalchemy import text,insert
from prettytable import PrettyTable
from sqlalchemy.exc import CompileError
from main import *
from utils import catch

import re




class ManagerDB:
    # Session = scoped_session(sessionmaker(engine))
    SQL = {
        'delete': ("DELETE FROM %s WHERE %s",2),
        'filter':("SELECT * FROM %s WHERE %s",2),
        'update':("UPDATE %s SET %s WHERE %s",3),
        'insert': ("INSERT INTO %s %s VALUES %s",3)
    }

    def __init__(self,table = None):
        if not issubclass(table,Base):
            raise ValueError('Нужно передать класс таблицы')
        self.table=table
        self.prettytable = PrettyTable()
        self.prettytable.field_names = self.table.get_columns
        self.compile = re.compile(r"\b(\w[^\s\.]+?)\b\s*=\s*(?P<q>[\"'])?(?(q)(.*?[\"'])|(.+?)\b)")


    def get(self, id):
        user = Session.get(self.table,id)
        return user


    def all(self):
        self._add_rows(
            [
                record.get_values() for record in Session.query(self.table).all()
            ]
        )

    def _add_rows(self,lst_data):
        self.prettytable.add_rows(lst_data)
        print(self.prettytable)
        self.prettytable._rows.clear()


    def insert(self,fields = None,values = None):
        if values is None or fields is None:
            values = fields =tuple()

            groups = self.compile.findall(input('Введите поле=значение:'))

            for group in groups:
                fields+=(group[0],)
                values+=( ''.join(group[1:]),)
            values = '('+','.join(values)+')'
            fields = '('+','.join(fields)+')'
        self._change_or_receive('insert',self.table.__tablename__,
                                fields,values,save=True)


    def filter(self,condition = None):
        condition = input('Введите условие поиска: ') if condition is None else condition
        self._change_or_receive('filter',self.table.__tablename__,
                                condition)#input('Введите условие поиска: ')

    def update(self,condition = None, fields = None):

        condition = input('Для каких записей: ') if condition is None else condition
        fields = input('Какие поля обновлять: ') if fields is None else fields

        self._change_or_receive('update',
                                self.table.__tablename__, fields,
                                condition,save=True)#input('Какие поля обновлять: ')    input('Для каких записей: ')

    def delete(self,condition = None):
        condition = input('Какие записи удалить: ') if condition is None else condition

        self._change_or_receive('delete',
                                self.table.__tablename__,
                                condition,save=True)#input('Какие записи удалить: ')

    def _change_or_receive(self,name,*params,save=False):
        query,length = self.SQL[name]
        self._execute_query(query % params[:length], save=save)

    @catch
    def _execute_query(self,query : str ,save=False):
        cursor=Session.execute(text(query))
        if save:
            Session.commit()
        try:
            self._add_rows(
                cursor.all()
            )
        except:
            print('Операция выполнена')



class HistoryManagerDB(ManagerDB):

    def insert_order(self,data,user):
        for product,count in data.items():
            Session.add(self.table(
                user=user.username,
                product_name=product.product_name,
                price=product.price,
                count=count)
            )
        Session.commit()

    def print_user_history(self,user):
        pt = PrettyTable(('Product','Price (per one)','Count'))

        pt.add_rows(
            [record.get_values()[2:] for record in Session.query(self.table).filter(self.table.user==user.username).all()]
        )
        print(pt)

class UserManagerDB(ManagerDB):
    def change_username(self,user):
        username = input('Enter a new name: ')
        self._update_user(user,USERNAME_FIELD,username)


    def change_password(self,user):
        password = input('Enter a new password: ')
        self._update_user(user,PASSWORD_FIELD,password)

    def _update_user(self,user,field,new_value):
        setattr(user,field,new_value)
        Session.commit()
        print('Изменения сохранены!')

