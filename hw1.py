import json
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/sales'
engine = create_engine(db_url)

Base = declarative_base()

class Sales(Base):
    __tablename__ = 'sales'
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