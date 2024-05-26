from sqlalchemy import create_engine, Column, Integer, String, Sequence, Date
from sqlalchemy import or_, and_, func
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
# person1 = Person(first_name="John", last_name="Smith",
#                  city="Kyiv", country="Ukraine", birth_date='01-01-2000')
# person2 = Person(first_name="Mary", last_name="Smith",
#                  city="Kyiv", country="Ukraine", birth_date='01-01-2000')
#
# session.add_all([person1, person2])
# # session.add(person1)
# # session.add(person2)
# session.commit()

while True:
    print("Введіть команду")
    print("1 виконати запит")
    print("2 вивести всіх людей")
    print("3 вивести людей з певного міста")
    print("4 вивести людей з певного міста або країни")
    print("5 вивести людей ім'я яких плчинається з певної літери")
    print('6 добавити нову людину')
    print('7 внести зміни до запису')
    print('8 видалити запис')

    command = input('номер команди:')

    if command == 'exit':
        break

    if command == '1':
        user_query = input('введіть запит ')
        result = session.execute(text(user_query))

        for person in result:
            print(person.first_name, person.last_name)

    elif command == '2':
        result = session.query(Person).all() # SELECT * FROM PERSON

        for person in result:
            print(person.first_name, person.last_name)

    elif command == '3':
        city = input('введіть назву міста: ')

        # result = session.query(Person).filter_by(city=city).all()
        result = session.query(Person).filter(Person.city == city).all()

        for person in result:
            print(person.first_name, person.last_name)

    elif command == '4':
        city = input('введіть назву міста: ')
        country = input('введіть назву країни: ')

        result = session.query(Person).filter(or_(
            Person.city == city,
            Person.country == country
        ))

        for person in result:
            print(person.first_name, person.last_name)

    elif command == '5':
        letter = input('введіть літеру: ')
        # J  -> fist_name like 'J%'
        result = session.query(Person).filter(
            Person.first_name.like(f'{letter}%')
        )

        for person in result:
            print(person.first_name, person.last_name)

    elif command == '6':
        person = Person(first_name = input("введіть ім'я: "),
                        last_name = input("введіть прізвище: "),
                        city = input("введіть місто: "),
                        country = input("введіть країна: "),
                        birth_date = input("введіть дата народження: "),
        )

        session.add(person)
        session.commit()

    elif command == '7':
        first_name = input("введіть ім'я: ")

        person = session.query(Person).filter(
            Person.first_name == first_name
        ).first()

        person.city = input("введіть нове місто")

        session.commit()

        # persons = session.query(Person).filter(
        #     Person.first_name == first_name
        # ).all()
        #
        # for person in persons:
        #     person.country = ...
        #
        # session.commit()

    elif command == '8':
        first_name = input("введіть ім'я: ")

        person = session.query(Person).filter(
            Person.first_name == first_name
        ).first()

        session.delete(person)
        session.commit()

session.close()