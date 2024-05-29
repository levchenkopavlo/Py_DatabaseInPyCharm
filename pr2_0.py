from sqlalchemy import create_engine, MetaData, insert, delete, update
from sqlalchemy.orm import sessionmaker
import json


with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

db_url = f'postgresql+pg8000://{db_user}:{db_password}@localhost:5432/hospital'
engine = create_engine(db_url)

metadata = MetaData()
metadata.reflect(bind=engine)

connection = engine.connect()


def insert_row(table):
    values = {}

    for column_name in table.columns.keys():
        value = input(f'Введіть значення для стовпчика {column_name}: ')

        if value != '':
            values[column_name] = value

    query = insert(table).values(values)
    connection.execute(query)
    connection.commit()

    print('Everything is OK')


def update_data(table):
    print('назви стовпчиків')
    for column_name in table.columns.keys():
        print('\t', column_name)

    condition_column = input('введіть назву стовпчика для умови: ')
    condition_value = input('введіть значення для вказаного стовпчика для умови: ')

    # update where column==value
    values = {}

    for column_name in table.columns.keys():
        value = input(f'Введіть значення для стовпчика {column_name}: ')

        if value != '':
            values[column_name] = value

    column = getattr(table.c, condition_column)

    query = update(table) \
            .where(column == column.type.python_type(condition_value)) \
            .values(values)

    connection.execute(query)
    connection.commit()


def delete_data(table):
    print('назви стовпчиків')
    for column_name in table.columns.keys():
        print('\t', column_name)

    # condition_column = input('введіть назву стовпчика для умови: ')
    # condition_value = input('введіть значення для вказаного стовпчика для умови: ')
    #
    # column = getattr(table.c, condition_column)
    #
    # query = delete(table).where(column == column.type.python_type(condition_value))

    condition = input('введіть умову для одного стовпчика')
    # premium < 20

    query = delete(table).where(eval('table.c.' + condition))

    connection.execute(query)
    connection.commit()


while True:
    print('Таблиці з бази даних')
    for table_name in metadata.tables.keys():
        print(table_name)

    table_name = input('Введіть назву таблиці: ')

    if table_name in metadata.tables:
        table = metadata.tables[table_name]

        print('Оберіть функцію')
        print('1 добавити рядок')
        print('2 видалити дані')
        print('3 змінити дані')

        command = int(input('Номер функції: '))

        if command == 1:
            insert_row(table)
        elif command == 2:
            delete_data(table)
        elif command == 3:
            update_data(table)