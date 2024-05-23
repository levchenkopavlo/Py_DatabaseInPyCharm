from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
import json

with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/test'
engine = create_engine(db_url)

Base = declarative_base()


# створення таблиці users
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(20))
    age = Column(Integer)


# добавляємо таблиці
Base.metadata.create_all(bind=engine)

#
# data = {}
# data['user'] = 'postgres'
# data['password'] = 'postgres'
# with open('config.json', 'w') as f:
#     json.dump(data, f)
