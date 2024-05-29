"""Завдання 3"""
from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy import Column, Integer, String, Float
import json

# Зчитування конфігураційних даних з файлу
with open('config.json') as f:
    config = json.load(f)

# Отримання логіну та паролю з об'єкта конфігурації
db_user = config['database']['user']
db_password = config['database']['password']

# Побудова URL для підключення до PostgreSQL
db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Hospital'
engine = create_engine(db_url)

# З'єднання з базою даних
conn = engine.connect()
metadata = MetaData()

# Завантаження таблиць
# Автоматично завантажує всі таблиці
metadata.reflect(bind=engine)

# Створення об'єкту сесії для взаємодії з базою даних
Session = sessionmaker(bind=engine)
session = Session()
# Функція для відображення назв усіх таблиць
def display_tables():
    print("Tables in the database:")
    for table_name in metadata.tables.keys():
        print(table_name)

# Функція для відображення назв стовпців певної таблиці
def display_columns(table_name):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        print(f"Columns in table {table_name}:")
        for column in table.columns:
            print(column.name)
    else:
        print(f"Table {table_name} not found.")

# Функція для відображення назв стовпців та їх типів для певної таблиці
def display_column_types(table_name):
    if table_name in metadata.tables:
        table = metadata.tables[table_name]
        print(f"Columns and their types in table {table_name}:")
        for column in table.columns:
            print(f"{column.name}: {column.type}")
    else:
        print(f"Table {table_name} not found.")

# Функція для відображення зв’язків між таблицями
def display_relationships_tables():
    inspector = inspect(engine)
    print("Relationships between tables:")
    for table_name in metadata.tables.keys():
        foreign_keys = inspector.get_foreign_keys(table_name)
        if foreign_keys:
            print(f"Table {table_name}:")
            for foreign_key in foreign_keys:
                print(f"  -> References {foreign_key['referred_table']}({', '.join(foreign_key['referred_columns'])})")

def create_table():
    table_name = input("Введіть назву нової таблиці: ")

    # Перевіряємо, чи така таблиця ще не існує
    if table_name in metadata.tables:
        print(f"Таблиця {table_name} вже існує.")
        return

    # Створюємо список для зберігання стовпців
    columns = []

    # Просимо користувача ввести назви та типи стовпців
    while True:
        column_name = input("Введіть назву стовпця (або 'готово', щоб завершити): ")
        if column_name.lower() == 'готово':
            break

        column_type = input("Введіть тип стовпця (наприклад, Integer, String, Float): ")

        # Додаємо стовпець до списку
        columns.append(Column(column_name, eval(column_type)))

    # Створюємо об'єкт таблиці
    new_table = Table(
        table_name,
        metadata,
        *columns  # Розпаковуємо список стовпців
    )

    # Створюємо таблицю в базі даних
    new_table.create(bind=engine)  # Використовуємо bind для підключення до бази даних

    print(f"Таблицю {table_name} створено успішно.")

def delete_table():
    table_name = input("Введіть назву таблиці, яку бажаєте видалити: ")

    # Перевіряємо, чи таблиця існує
    if table_name in metadata.tables:
        # Видаляємо таблицю з бази даних
        metadata.tables[table_name].drop(bind=engine)
        print(f"Таблицю {table_name} видалено успішно.")
    else:
        print(f"Таблиці {table_name} не існує.")

def add_column_table():
    table_name = input("Введіть назву таблиці, до якої бажаєте додати стовпець: ")

    # Перевіряємо, чи таблиця існує
    if table_name in metadata.tables:
        # Отримуємо існуючий об'єкт Table
        existing_table = metadata.tables[table_name]

        # Запитуємо в користувача назву та тип нового стовпця
        while True:
            column_name = input("Введіть назву стовпця (або 'готово', щоб завершити): ")
            if column_name.lower() == 'готово':
                break

            column_type = input("Введіть тип стовпця (наприклад, Integer, String, Float): ")

            # Створюємо новий об'єкт Column
            new_column = Column(column_name, eval(column_type))

            # Створюємо новий об'єкт Table з новим стовпцем та існуючими
            new_table = Table(
                table_name,
                metadata,
                Column('id', Integer, primary_key=True),
                *existing_table.columns,
                new_column,
                extend_existing=True  # Додаємо параметр extend_existing
            )

            # Видаляємо існуючу таблицю
            existing_table.drop(bind=engine, checkfirst=True)

            # Створюємо нову таблицю з новими стовпцями
            new_table.create(bind=engine, checkfirst=True)

            print(f"Стовпець {column_name} успішно додано до таблиці {table_name}.")
    else:
        print(f"Таблиці {table_name} не існує.")

while True:
    print("1. відобразити назви усіх таблиць")
    print("2. відобразити назви стовпців певної таблиці")
    print("3. відобразити назви стовпців та їх типи для певної таблиці")
    print("4. відобразити зв’язки між таблицями")
    print("5. створити таблицю")
    print("6. видалити таблицю")
    print("7. додати стовбець до вказаної таблиці")

    print("0. Вийти")
    choice = input("Оберіть опцію: ")

    if choice == "1":
        display_tables()
    elif choice == "2":
        table_name = input("Введіть назву таблиці: ")
        display_columns(table_name)
    elif choice == "3":
        table_name = input("Введіть назву таблиці: ")
        display_column_types(table_name)
    elif choice == "4":
        display_relationships_tables()
    elif choice == "5":
        create_table()
    elif choice == "6":
        delete_table()
    elif choice == "7":
        add_column_table()

    elif choice == "0":
        break
    else:
        print("Невірний вибір. Будь ласка, оберіть знову.")

# Закриваємо сесію
session.close()