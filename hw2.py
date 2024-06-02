from sqlalchemy import create_engine, inspect, MetaData, Table, Column, Integer, String, ForeignKey, func, and_
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
lectures = metadata.tables['lectures']
groupslectures = metadata.tables['groupslectures']
subjects = metadata.tables['subjects']

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
        result = session.query(groups.c.id, groups.c.name, groups.c.rating, groups.c.year,
                               departments.c.name.label('department')).join(departments,
                                                                            departments.c.id == groups.c.departmentid).all()
        if result:
            for row in result:
                print(
                    f"id: {row.id}, name: {row.name}, rating: {row.rating}, year: {row.year}, department: {row.department}")

    # 2. вивести інформацію про всіх викладачів
    elif command == '2':
        result = session.query(teachers).all()
        if result:
            for row in result:
                for column_name in teachers.columns.keys():
                    print(f'{column_name}, {row.__getattr__(column_name)}', end='; ')
                print()

    # 3. вивести назви усіх кафедр
    elif command == '3':
        result = session.query(departments, faculties.c.name.label('faculty')) \
            .join(faculties, faculties.c.id == departments.c.facultyid).all()
        if result:
            for row in result:
                print(f"{row.name}")

    # 4. вивести імена та прізвища викладачів, які читають лекції в конкретній групі
    elif command == '4':
        group = input('Введіть назву групи: ')
        result = session.query(teachers.c.name, teachers.c.surname) \
            .join(lectures, lectures.c.teacherid == teachers.c.id) \
            .join(groupslectures, groupslectures.c.lectureid == lectures.c.id) \
            .join(groups, groups.c.id == groupslectures.c.groupid) \
            .where(func.lower(groups.c.name) == group.lower())
        if result:
            for row in result:
                print(f"{row.name} {row.surname}")

    # 5. вивести назви кафедр і груп, які до них відносяться')
    elif command == '5':
        result = session.query(departments.c.name.label('department'), groups.c.name.label('group')) \
            .join(groups, departments.c.id == groups.c.departmentid).all()
        if result:
            for row in result:
                print(f"{row.department} {row.group}")

    # 6. відобразити кафедру з максимальною кількістю груп
    elif command == '6':
        dep_by_groups = session.query(departments.c.name.label('department'), departments.c.id.label('department_id'),
                                      func.count(departments.c.name).label('count')) \
            .join(groups, departments.c.id == groups.c.departmentid) \
            .group_by(departments.c.id).subquery()
        max_groups = session.query(func.max(dep_by_groups.c.count)).scalar()
        result = session.query(dep_by_groups).where(dep_by_groups.c.count == max_groups).all()
        if result:
            for row in result:
                print(f"{row.department}")

    # 7. відобразити кафедру з мінімальною кількістю груп
    elif command == '7':
        dep_by_groups = session.query(departments.c.name.label('department'), departments.c.id.label('department_id'),
                                      func.count(departments.c.name).label('count')) \
            .join(groups, departments.c.id == groups.c.departmentid) \
            .group_by(departments.c.id).subquery()
        min_groups = session.query(func.min(dep_by_groups.c.count)).scalar()
        result = session.query(dep_by_groups).where(dep_by_groups.c.count == min_groups).all()
        if result:
            for row in result:
                print(f"{row.department}")

    # 8. вивести назви предметів, які викладає конкретний викладач
    elif command == '8':
        # teacher = input('Введіть ім\'я та прізвище викладача: ')
        teacher = 'john doe'
        result = session.query(subjects) \
            .join(lectures, subjects.c.id == lectures.c.subjectid) \
            .join(teachers, teachers.c.id == lectures.c.teacherid) \
            .where(func.lower(teachers.c.name + ' ' + teachers.c.surname) == teacher.lower()).all()
        if result:
            for row in result:
                print(f"{row.name}")

    # 9. вивести назви кафедр, на яких викладається конкретна дисципліна
    elif command == '9':
        subject = input('Введіть назву предмета: ')
        # subject = 'Engineering'
        result = session.query(departments) \
            .join(groups, groups.c.departmentid == departments.c.id) \
            .join(groupslectures, groupslectures.c.groupid == groups.c.id) \
            .join(lectures, lectures.c.id == groupslectures.c.lectureid) \
            .join(subjects, subjects.c.id == lectures.c.subjectid) \
            .where(func.lower(subjects.c.name) == subject.lower()).all()
        if result:
            for row in result:
                print(f"{row.name}")

    # 10. вивести назви груп, що належать до конкретного факультету
    elif command == '10':
        faculty = input('Введіть назву факультету: ')
        # faculty = 'Engineering'
        result = session.query(groups) \
            .join(departments, departments.c.id == groups.c.departmentid) \
            .join(faculties, faculties.c.id == departments.c.facultyid) \
            .where(func.lower(faculties.c.name) == faculty.lower()).all()
        if result:
            for row in result:
                print(f"{row.name}")

    # 11. вивести назви предметів та повні імена викладачів, які читають найбільшу кількість лекцій з них
    elif command == '11':
        summary_data = session.query(subjects.c.name.label('subject'), subjects.c.id.label('subjectid'),
                                     func.count(teachers.c.id).label('count'),
                                     (teachers.c.name + ' ' + teachers.c.surname).label('teacher'),
                                     teachers.c.id.label('teacherid')) \
            .join(lectures, subjects.c.id == lectures.c.subjectid) \
            .join(teachers, lectures.c.teacherid == teachers.c.id) \
            .group_by(subjects.c.name, teachers.c.id, subjects.c.id).subquery()

        subjects_in_summary = session.query(summary_data.c.subject, summary_data.c.subjectid).distinct().order_by(
            summary_data.c.subject)

        if subjects_in_summary:
            for row in subjects_in_summary:
                # print(row.subject)
                max_for_subject = session.query((func.max(summary_data.c.count)).label('max'), summary_data.c.subjectid).where(
                    summary_data.c.subjectid == row.subjectid).subquery()
                # print(max_for_subject)

                result = session.query(summary_data.c.subject, summary_data.c.teacher).where(
                    and_(summary_data.c.count == max_for_subject.c.max, summary_data.c.subjectid == max_for_subject.c.subjectid)).all()
                if result:
                    for row_int in result:
                        print(f'{row_int.subject} - {row_int.teacher}')


    # 12. вивести назву предмету, за яким читається найменше лекцій
    elif command == '12':
        lecture_by_subject = session.query(lectures.c.subjectid.label('subject_id'),
                                           func.count(lectures.c.subjectid).label('count')) \
            .group_by(lectures.c.subjectid).subquery()
        min_lectures = session.query(func.min(lecture_by_subject.c.count)).scalar()
        result = session.query(lecture_by_subject, subjects.c.name).join(subjects,
                                                                         subjects.c.id == lecture_by_subject.c.subject_id) \
            .where(lecture_by_subject.c.count == min_lectures)
        if result:
            for row in result:
                print(f"{row.name}")
    # 13. вивести назву предмету, за яким читається найбільше лекцій
    elif command == '13':
        lecture_by_subject = session.query(lectures.c.subjectid.label('subject_id'),
                                           func.count(lectures.c.subjectid).label('count')) \
            .group_by(lectures.c.subjectid).subquery()
        max_lectures = session.query(func.max(lecture_by_subject.c.count)).scalar()
        result = session.query(lecture_by_subject, subjects.c.name).join(subjects,
                                                                         subjects.c.id == lecture_by_subject.c.subject_id) \
            .where(lecture_by_subject.c.count == max_lectures)
        if result:
            for row in result:
                print(f"{row.name}")
