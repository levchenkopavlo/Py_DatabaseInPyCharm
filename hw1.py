import json
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Date, DECIMAL, VARCHAR, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/sales'
engine = create_engine(db_url)

Base = declarative_base()


class Salesmen(Base):
    __tablename__ = 'salesmen'
    id = Column(Integer, Sequence('salesmen_id_seq'), primary_key=True)
    salesman_acc = Column(VARCHAR, nullable=False, unique=True)

    sale = relationship("Sales", back_populates="salesman")


class Customers(Base):
    __tablename__ = 'customers'
    id = Column(Integer, Sequence('cutomer_id_seq'), primary_key=True)
    customer_acc = Column(VARCHAR, nullable=False, unique=True)

    sale = relationship("Sales", back_populates="customer")


class Sales(Base):
    __tablename__ = 'sales'
    id = Column(Integer, Sequence('sale_id_seq'), primary_key=True)
    amount = Column(DECIMAL(10, 2))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    salesmen_id = Column(Integer, ForeignKey('salesmen.id'))
    date = Column(Date)

    salesman = relationship("Salesmen", back_populates="sale")
    customer = relationship("Customers", back_populates="sale")


# добавляємо таблиці
Base.metadata.create_all(bind=engine)

# створення сесії
Session = sessionmaker(bind=engine)
session = Session()

while True:
    print("Введіть команду")
    print("1 додати дані")
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
    elif command == '1':
        while True:
            print("Введіть команду або Enter для виходу")
            print("1 додати покупця")
            print("2 додати продавця")
            print("3 додати інформацію про продаж")
            command = input('номер команди:')
            if command == '':
                break
            elif command == '1':
                person = Customers(customer_acc=input("введіть логін покупця: "))
                if session.query(Customers).filter(Customers.customer_acc == person.customer_acc).all():
                    pass
                else:
                    session.add(person)

            elif command == '2':
                salesman = Salesmen(salesman_acc=input("введіть логін продавця: "))
                if not session.query(Salesmen).filter(Salesmen.salesman_acc == salesman.salesman_acc).all():
                    session.add(salesman)
            elif command == '3':
                sale = Sales(date=input("введіть дату продажу: "), amount=input("введіть суму продажу: "))
                while True:
                    salesman = input("введіть логін продавця: ")
                    if session.query(Salesmen).filter(Salesmen.salesman_acc == salesman).all():
                        break
                    else:
                        print('Продавця не знайдено. Повторіть')

                person = Customers(customer_acc=input("введіть логін покупця: "))
            session.commit()