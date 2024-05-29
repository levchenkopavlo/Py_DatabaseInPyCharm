from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy.orm import sessionmaker, relationship, aliased
from sqlalchemy import Column, Integer, String, Float
import json

# Зчитування конфігураційних даних з файлу
with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

# Побудова URL для підключення до PostgreSQL
db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/academy'
engine = create_engine(db_url)

# З'єднання з базою даних
metadata = MetaData()
metadata.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

connection = engine.connect()

groups = metadata.tables['groups']
departments = metadata.tables['departments']
faculties = metadata.tables['faculties']
teachers = metadata.tables['teachers']


# print('Таблиці з бази даних')
# for table_name in metadata.tables.keys():
#     print(table_name)

while True:
    print('1. вивести інформацію про всі навчальні групи')
    print('2. вивести інформацію про всіх викладачів')
    print('3. вивести назви усіх кафедр')
    print('4. вивести імена та прізвища викладачів, які читають лекції в конкретній групі')
    print('5. вивести назви кафедр і груп, які до них відносяться')
    print('6. відобразити кафедру з максимальною кількістю груп')
    print('7. відобразити кафедру з мінімальною кількістю груп')
    print('8. вивести назви предметів, які викладає конкретний викладач')
    print('9. вивести назви кафедр, на яких викладається конкретна дисципліна')
    print('10. вивести назви груп, що належать до конкретного факультету')
    print('11. вивести назви предметів та повні імена викладачів, які читають найбільшу кількість лекцій з них')
    print('12. вивести назву предмету, за яким читається найменше лекцій')
    print('13. вивести назву предмету, за яким читається найбільше лекцій')

    command = input('Оберіть функцію: ')
    if command == 'exit' or command == '':
        session.close()
        break

    # 1. вивести інформацію про всі навчальні групи
    elif command == '1':
        result = session.query(groups.c.id, groups.c.name, groups.c.rating, groups.c.year, departments.c.name.label('department')).join(departments, departments.c.id == groups.c.departmentid).all()
        if result:
            for row in result:
                print(f"id: {row.id}, name: {row.name}, rating: {row.rating}, year: {row.year}, department: {row.department}")

    # 2. вивести інформацію про всіх викладачів
    elif command == '2':
        result = session.query(teachers).all()
        if result:
            for row in result:


    # 3. вивести назви усіх кафедр
    elif command == '3':
        result = session.query(departments, faculties.c.name.label('faculty')).join(faculties, faculties.c.id == departments.c.facultyid).all()
        if result:
            for row in result:
                # print(f"id: {row.id}, name: {row.name}, building: {row.building}, financing: {row.financing}, faculty: {row.faculty}")
                print(f"{row.name}")