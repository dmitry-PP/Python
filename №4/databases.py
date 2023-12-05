from sqlalchemy import MetaData,Table,Column,Integer,String,ForeignKey,Text,Boolean
from sqlalchemy.orm import relationship
from manager import ManagerDB,HistoryManagerDB,UserManagerDB
from main import *
from utils import add_manager
from mixins import GetColumnMixin




class Base(Base):
    __abstract__ = True
    __NAMES_TABLES = dict()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Base.__NAMES_TABLES[cls.__tablename__] = cls


@add_manager(UserManagerDB)
class User(GetColumnMixin,Base):
    __tablename__ = 'user'

    id = Column(Integer,primary_key=True,autoincrement=True,unique=True,nullable=False)
    username = Column(String(25),unique=True,nullable=False)
    password = Column(String(100),nullable=False)
    roll = relationship('Roll',backref='user',lazy='subquery')
    roll_id = Column(Integer,ForeignKey('roll.id'))


    def __str__(self):
        return f'User<id={self.id},username={self.username}>'

@add_manager(ManagerDB)
class Roll(GetColumnMixin,Base):
    __tablename__ = 'roll'

    id = Column(Integer,primary_key=True,autoincrement=True,unique=True,nullable=False)
    name = Column(String(40),nullable=False)


    def __str__(self):
        return f'Roll<id={self.id},roll_name={self.name}>'

@add_manager(ManagerDB)
class Store(GetColumnMixin,Base):
    __tablename__ = 'store'

    id = Column(Integer,primary_key=True,autoincrement=True,unique=True,nullable=False)
    product_name = Column(String(50),nullable=False)
    description = Column(Text,nullable=True)
    price = Column(Integer,nullable=False)
    count = Column(Integer,nullable=False,default=0)
    availability = Column(Boolean,default=False,nullable=False)


    def __str__(self):
        return f'Store<id={self.id},product_name={self.product_name}>'


@add_manager(HistoryManagerDB)
class History(GetColumnMixin,Base):
    __tablename__ = 'history'

    id = Column(Integer,primary_key=True,autoincrement=True,unique=True,nullable=False)
    user = Column(String(25),nullable=False)
    product_name = Column(String(50), nullable=False)
    price = Column(Integer,nullable=False)
    count = Column(Integer,nullable=False)



    def __str__(self):
        return f'History<id={self.id},user_id={self.user_id},store_id={self.store_id}>'

Base.metadata.create_all(engine)



