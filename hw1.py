import json
from sqlalchemy import create_engine, Column, Integer, Sequence, String, Date, DECIMAL, VARCHAR, ForeignKey, func
from sqlalchemy import and_, or_
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
    print("1 додати покупця")
    print("2 додати продавця")
    print("3 додати інформацію про продаж")
    print("4 редагувати покупця")
    print("5 редагувати продавця")
    print("6 редагувати інформацію про продаж")
    print("7 видалити покупця")
    print("8 видалити продавця")
    print("9 видалити інформацію про продаж")
    print("10 Відображення усіх угод")
    print('11 Відображення угод конкретного продавця;')
    print('12 Відображення максимальної за сумою угоди')
    print('13 Відображення мінімальної за сумою угоди;')
    print('14 Відображення максимальної суми угоди для конкретного продавця;')
    print('15 Відображення мінімальної за сумою угоди для конкретного продавця;')
    print('16 Відображення максимальної за сумою угоди для конкретного покупця;')
    print('17 Відображення мінімальної за сумою угоди для конкретного покупця;')
    print('18 Відображення продавця з максимальною сумою продажів за всіма угодами;')
    print('19 Відображення продавця з мінімальною сумою продажів за всіма угодами;')
    print('20 Відображення покупця з максимальною сумою покупок за всіма угодами;')
    print('21 Відображення середньої суми покупки для конкретного покупця;')
    print('22 Відображення середньої суми покупки для конкретного продавця"')

    command = input('номер команди:')

    if command == 'exit' or command == '':
        session.close()
        break
    elif command == '1':
        customer = Customers(customer_acc=input("введіть логін покупця: "))
        if session.query(Customers).filter(Customers.customer_acc == customer.customer_acc).all():
            pass
        else:
            session.add(customer)
            session.commit()

    elif command == '2':
        salesman = Salesmen(salesman_acc=input("введіть логін продавця: "))
        if not session.query(Salesmen).filter(Salesmen.salesman_acc == salesman.salesman_acc).all():
            session.add(salesman)
            session.commit()

    elif command == '3':
        sale = Sales(date=input("введіть дату продажу: "), amount=input("введіть суму продажу: "))
        while True:
            salesman = input("введіть логін продавця: ")
            result = session.query(Salesmen).filter(Salesmen.salesman_acc == salesman).all()
            if result:
                sale.salesmen_id = result[0].id
                break
            else:
                print('Продавця не знайдено. Повторіть')
        while True:
            customer = input("введіть логін покупця: ")
            result = session.query(Customers).filter(Customers.customer_acc == customer).all()
            if result:
                sale.customer_id = result[0].id
                break
            else:
                print('Покупця не знайдено. Повторіть')
        session.add(sale)
        session.commit()
    elif command == '4':
        customer = input("введіть логін покупця: ")
        result = session.query(Customers).filter(Customers.customer_acc == customer).all()
        if result:
            while True:
                customer = input("введіть новий логін покупця: ")
                if customer:
                    print(len(result))
                    result[0].customer_acc = customer
                    session.commit()
                    break
    elif command == '5':
        salesman = input("введіть логін продавця: ")
        result = session.query(Salesmen).filter(Salesmen.salesman_acc == salesman).all()
        if result:
            while True:
                salesman = input("введіть новий логін покупця: ")
                if salesman:
                    print(len(result))
                    result[0].customer_acc = salesman
                    session.commit()
                    break
    elif command == '6':
        deal_id = input("введіть id продажу: ")
        result = session.query(Sales).filter(Sales.id == deal_id).scalar()
        if result:
            customer_acc = input("введіть логін покупця: "),
            customer_id = session.query(Customers.id).filter(Customers.customer_acc == customer_acc).scalar()
            salesman_acc = input("введіть логін продавця: "),
            salesman_id = session.query(Salesmen.id).filter(Salesmen.salesman_acc == salesman_acc).scalar()
            date = input('введіть дату')
            amount = float(input('введіть суму продажу'))
            result.customer_id = customer_id
            result.salesmen_id = salesman_id
            result.date = date
            result.amount = amount
            session.commit()
    elif command == '7':
        customer = input("введіть логін покупця: ")
        result = session.query(Customers).filter(Customers.customer_acc == customer).all()
        session.delete(result)
        session.commit()
    elif command == '8':
        salesman = input("введіть логін продавця: ")
        result = session.query(Salesmen).filter(Salesmen.salesman_acc == salesman).all()
        session.delete(result)
        session.commit()
    elif command == '8':
        deal_id = input("введіть id продажу: ")
        result = session.query(Sales).filter(Sales.id == deal_id).all()
        session.delete(result)
        session.commit()

    # Відображення усіх угод
    elif command == '10':
        result = session.query(Sales).join(Salesmen).join(Customers).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення угод конкретного продавця
    elif command == '11':
        salesman = input("введіть логін продавця: ")
        result = session.query(Sales).join(Salesmen).join(Customers).filter(Salesmen.salesman_acc == salesman).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення максимальної за сумою угоди
    elif command == '12':
        max_sale = session.query(func.max(Sales.amount)).scalar()
        result = session.query(Sales).join(Salesmen).join(Customers).filter(Sales.amount == max_sale).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення мінімальної за сумою угоди;
    elif command == '13':
        min_sale = session.query(func.min(Sales.amount)).scalar()
        result = session.query(Sales).join(Salesmen).join(Customers).filter(Sales.amount == min_sale).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення максимальної суми угоди для конкретного продавця;
    elif command == '14':
        salesman = input("введіть логін продавця: ")
        max_sale = session.query(func.max(Sales.amount)).join(Salesmen).filter(
            Salesmen.salesman_acc == salesman).scalar()
        result = session.query(Sales).join(Salesmen).join(Customers).filter(
            and_(Sales.amount == max_sale, Salesmen.salesman_acc == salesman)).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення мінімальної за сумою угоди для конкретного продавця;
    elif command == '15':
        salesman = input("введіть логін продавця: ")
        min_sale = session.query(func.min(Sales.amount)).join(Salesmen).filter(
            Salesmen.salesman_acc == salesman).scalar()
        result = session.query(Sales).join(Salesmen).join(Customers).filter(
            and_(Sales.amount == min_sale, Salesmen.salesman_acc == salesman)).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення максимальної за сумою угоди для конкретного покупця;
    elif command == '16':
        customer = input("введіть логін покупця: ")
        max_sale = session.query(func.max(Sales.amount)).join(Customers).filter(
            Customers.customer_acc == customer).scalar()
        result = session.query(Sales).join(Salesmen).join(Customers).filter(
            and_(Sales.amount == max_sale, Customers.customer_acc == customer)).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення мінімальної за сумою угоди для конкретного покупця
    elif command == '17':
        customer = input("введіть логін покупця: ")
        min_sale = session.query(func.min(Sales.amount)).join(Customers).filter(
            Customers.customer_acc == customer).scalar()
        result = session.query(Sales).join(Salesmen).join(Customers).filter(
            and_(Sales.amount == min_sale, Customers.customer_acc == customer)).all()
        for item in result:
            print(item.id, item.amount, item.date, item.customer.customer_acc, item.salesman.salesman_acc)

    # Відображення продавця з максимальною сумою продажів за всіма угодами;
    elif command == '18':
        total_amount = session.query(Sales.salesmen_id, func.sum(Sales.amount).label('total_amount1')) \
            .group_by(Sales.salesmen_id).subquery()
        max_amount = session.query(func.max(total_amount.c.total_amount1).label('max_total_amount')).subquery()

        result = session.query(Salesmen.salesman_acc, total_amount.c.total_amount1) \
            .join(total_amount, Salesmen.id == total_amount.c.salesmen_id) \
            .filter(total_amount.c.total_amount1 == max_amount.c.max_total_amount).all()
        for item in result:
            print(item.salesman_acc, item.total_amount1)

    # Відображення продавця з мінімальною сумою продажів за всіма угодами;
    elif command == '19':
        total_amount = session.query(Sales.salesmen_id, func.sum(Sales.amount).label('total_amount1')) \
            .group_by(Sales.salesmen_id).subquery()
        min_amount = session.query(func.min(total_amount.c.total_amount1).label('min_total_amount')).subquery()

        result = session.query(Salesmen.salesman_acc, total_amount.c.total_amount1) \
            .join(total_amount, Salesmen.id == total_amount.c.salesmen_id) \
            .filter(total_amount.c.total_amount1 == min_amount.c.min_total_amount).all()
        for item in result:
            print(item.salesman_acc, item.total_amount1)

    # Відображення покупця з максимальною сумою покупок за всіма угодами;
    elif command == '20':
        total_amount = session.query(Sales.customer_id, func.sum(Sales.amount).label('total_amount1')) \
            .group_by(Sales.customer_id).subquery()
        max_amount = session.query(func.max(total_amount.c.total_amount1).label('max_total_amount')).subquery()

        result = session.query(Customers.customer_acc, total_amount.c.total_amount1) \
            .join(total_amount, Customers.id == total_amount.c.customer_id) \
            .filter(total_amount.c.total_amount1 == max_amount.c.max_total_amount).all()
        for item in result:
            print(item.customer_acc, item.total_amount1)

    # Відображення середньої суми покупки для конкретного покупця;
    elif command == '21':
        customer = input("введіть логін покупця: ")
        avg_amount = session.query(func.avg(Sales.amount)).join(Customers).filter(
            and_(Customers.customer_acc == customer)).scalar()
        print(avg_amount)

    # Відображення середньої суми покупки для конкретного продавця
    elif command == '22':
        salesman = input("введіть логін продавця: ")
        avg_amount = session.query(func.avg(Sales.amount)).join(Salesmen).filter(
            and_(Salesmen.salesman_acc == salesman)).scalar()
        print(avg_amount)
