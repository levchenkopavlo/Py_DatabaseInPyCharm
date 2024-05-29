from sqlalchemy import create_engine, MetaData, func, and_, or_, extract
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

Session = sessionmaker(bind=engine)
session = Session()


docs = metadata.tables['doctors']
specs = metadata.tables['specializations']
docsspecs = metadata.tables['doctorsspecializations']
doctors_vacations_table = metadata.tables['vacations']
Departments = metadata.tables['departments']
Sponsors = metadata.tables['sponsors']
Donations = metadata.tables['donations']
Wards = metadata.tables['wards']


# звіт 1
def report_doctor_specializations():
    result = session.query(docs.c.name.label('doctorname'),
                           docs.c.surname,
                           specs.c.specialization_name) \
             .join(docsspecs, docsspecs.c.doctor_id == docs.c.id) \
             .join(specs, docsspecs.c.specialization_id == specs.c.id).all()

    if result:
        for row in result:
            print(f"{row.doctorname} {row.surname} with specialization {row.specialization_name}")
    else:
        print('Пусто')

    # and - &
    # or - |
    # not - ~
    # (name == 'hjk') & (salary > 20)

#звіт 2
def report_doctors_salary_not_on_vacation():
    query = session.query(docs.c.surname, docs.c.salary) \
                   .outerjoin(doctors_vacations_table, (docs.c.id == doctors_vacations_table.c.doctor_id) &
                              ((doctors_vacations_table.c.start_date <= func.current_date()) & (func.current_date() <= doctors_vacations_table.c.end_date))) \
                   .filter(doctors_vacations_table.c.id == None)  # Фільтруємо тих, хто не в відпустці
    result = query.all()
    for row in result:
        print(f"{row.surname} - {row.salary}")

#звіт 3
def report_wards_depatment():
    department_name = input("Введіть назву відділення: ")

    query = session.query(Wards.c.name) \
        .join(Departments, Wards.c.department_id == Departments.c.id) \
        .filter(Departments.c.name == department_name)

    result = query.all()

    if result:
        print(f"Назви палат у відділенні '{department_name}':")
        for row in result:
            print(row.name)
    else:
        print(f"Відділення '{department_name}' або палати у цьому відділенні не знайдено.")

#звіт 4
def repor_donation_of_last_mounth():
    # Введіть номер місяця (1-12)
    month = int(input("Введіть номер місяця: "))

    query = session.query(Departments.c.name.label('Department'), Sponsors.c.name.label('Sponsor'),
                          Donations.c.amount.label('Amount'), Donations.c.date.label('DonationDate')) \
                   .join(Donations, Departments.c.id == Donations.c.department_id) \
                   .join(Sponsors, Sponsors.c.id == Donations.c.sponsor_id) \
                   .filter(extract('month', Donations.c.date) == month)

    result = query.all()

    if result:
        print(f"Усі пожертвування за {month}-й місяць:")
        for row in result:
            print(f"Відділення: {row.Department}, Спонсор: {row.Sponsor}, Сума: {row.Amount}, Дата: {row.DonationDate}")
    else:
        print(f"Пожертвувань за {month}-й місяць не знайдено.")
#звіт 5
def report_departaments_donation():
    sponsor_name = input("Введіть назву спонсора: ")

    query = session.query(Departments.c.name.label('Department')) \
                   .distinct() \
                   .join(Donations, Departments.c.id == Donations.c.department_id) \
                   .join(Sponsors, Sponsors.c.id == Donations.c.sponsor_id) \
                   .filter(Sponsors.c.name == sponsor_name)

    result = query.all()

    if result:
        print(f"Назви відділень, які спонсоруються компанією '{sponsor_name}':")
        for row in result:
            print(row.Department)
    else:
        print(f"Відділень, які спонсоруються компанією '{sponsor_name}' не знайдено.")


while True:
    print("1. Вивести повні імена лікарів та їх спеціалізації")
    print("2. Вивести прізвища та зарплати лікарів, які не перебувають у відпустці")
    print("3. Вивести назви палат, які знаходяться у певному відділенні;")
    print("4. Вивести усі пожертвування за вказаний місяць у вигляді: відділення, спонсор, сума пожертвування, дата пожертвування;")
    print("5. Вивести назви відділень без повторень, які спонсоруються певною компанією.")

    print("0. Вийти")
    choice = input("Оберіть опцію: ")

    if choice == "1":
        report_doctor_specializations()
    elif choice == "2":
        report_doctors_salary_not_on_vacation()
    elif choice == "3":
        report_wards_depatment()
    elif choice == "4":
        repor_donation_of_last_mounth()
    elif choice == "5":
        report_departaments_donation()

    elif choice == "0":
        break
    else:
        print("Невірний вибір. Будь ласка, оберіть знову.")

# Закриваємо сесію
session.close()