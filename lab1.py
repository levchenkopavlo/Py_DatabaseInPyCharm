from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import text
import json

with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/people'
engine = create_engine(db_url)

Base = declarative_base()


# створення таблиці users
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    city = Column(String(50))
    country = Column(String(50))
    birth_date = Column(Date)


# добавляємо таблиці
Base.metadata.create_all(bind=engine)

# створення сесії
Session = sessionmaker(bind=engine)
session = Session()

# добавлення рядків
person1 = Person(first_name="John", last_name="Smith",
                 city="Kyiv", country="Ukraine", birth_date='01-01-2000')
person2 = Person(first_name="Mary", last_name="Smith",
                 city="Kyiv", country="Ukraine", birth_date='01-01-2000')

session.add_all([person1, person2])
# session.add(person1)
# session.add(person2)
session.commit()