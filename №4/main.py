from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.orm import declarative_base




Base = declarative_base()
DATABASE = 'sqlite:///DB.db'

engine = create_engine(DATABASE)
Session = scoped_session(sessionmaker(engine))

PASSWORD_FIELD = 'password'
USERNAME_FIELD = 'username'



