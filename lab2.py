from sqlalchemy import create_engine, MetaData, func, and_, or_
from sqlalchemy.orm import sessionmaker
import json

with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/Hospital'
engine = create_engine(db_url)

metadata = MetaData()
metadata.reflect(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

docs = metadata.tables['doctors']
specs = metadata.tables['specializations']
docsspecs = metadata.tables['doctorsspecializations']
vacations = metadata.tables['vacations']
wards = metadata.tables['wards']
departments = metadata.tables['departments']
donations = metadata.tables['donations']
sponsors = metadata.tables['sponsors']


def report_doctor_specializations():
    result = session.query(docs.c.name.label('doctorname'),
                           docs.c.surname,
                           specs.c.specialization_name) \
        .join(docsspecs, docsspecs.c.doctor_id == docs.c.id) \
        .join(specs, docsspecs.c.specialization_id == specs.c.id).all()

    if result:
        for row in result:
            print(f"{row.doctorname} {row.surname} with specialization {row.specialization_name}")

    # and - &
    # or - |
    # (name == 'hjk') & (salary > 20)


def report_doctors_salary_not_on_vacation():
    result = session.query(docs.c.surname, docs.c.salary, docs.c.premium) \
        .outerjoin(vacations, ((vacations.c.doctor_id == docs.c.id) & (
                (func.current_date() < vacations.c.start_date) | (func.current_date() > vacations.c.end_date))) | (
                               vacations.c.doctor_id == None)).all()
    if result:
        for row in result:
            print(f"{row.doctorname} {row.surname} {row.salary} {row.premium}")


def report_wards_depatment():
    # department = input("введіть назву відділення: ")
    department = 'Cardiology'
    result = session.query(wards.c.name).join(departments, departments.c.id == wards.c.department_id).where(
        departments.c.name == department)
    if result:
        for row in result:
            print(f"{row.name}")


def repor_donation_of_last_mounth():
    month = 1
    result = session.query(departments.c.name, sponsors.c.sponsor_name, donations.c.donation_amount,
                           donations.c.donation_date) \
        .join(donations, donations.c.department_id == departments.c.id) \
        .join(sponsors, sponsors.c.id == donations.c.sponsor_id) \
        .filter(func.extract('month', donations.c.donation_date) == month).all()


def report_departaments_donation():
    result = session.query(departments.c.name) \
        .join(donations, donations.c.department_id == departments.c.id) \
        .join(sponsors, sponsors.c.id == donations.c.sponsor_id) \
        .all()
    if result:
        for row in result:
            print(f"{row.name}")


while True:
    print("1. Вивести повні імена лікарів та їх спеціалізації")
    print("2. Вивести прізвища та зарплати лікарів, які не перебувають у відпустці")
    print("3. Вивести назви палат, які знаходяться у певному відділенні;")
    print(
        "4. Вивести усі пожертвування за вказаний місяць у вигляді: відділення, спонсор, сума пожертвування, дата пожертвування;")
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
