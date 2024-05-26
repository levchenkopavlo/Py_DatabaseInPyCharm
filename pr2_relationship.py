from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Sequence
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
import json

with open('config.json', 'r') as f:
    data = json.load(f)
    db_user = data['user']  # postgres
    db_password = data['password']

db_url = f'postgresql+psycopg2://{db_user}:{db_password}@localhost:5432/people'
engine = create_engine(db_url)

# Оголошення базового класу
Base = declarative_base()


# Визначення класу моделі для користувачів
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(50))

    projects = relationship('Project', back_populates='users',
                            secondary='user_projects')


# Визначення класу моделі для проектів
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, Sequence('project_id_seq'), primary_key=True)
    name = Column(String(100), unique=True)

    users = relationship("User", # назва класу з яким поєднується
                         back_populates='projects', # зв'язок з таблиці users
                         secondary='user_projects'  # таблиця user_projects
                         )


# Визначення асоціаційної таблиці
class UserProject(Base):
    __tablename__ = 'user_projects'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id'), primary_key=True)


Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

# Додавання користувачів та проектів
user1 = User(username='john_doe', email='john@example.com', password='password123')
user2 = User(username='jane_doe', email='jane@example.com', password='pass456')

project1 = Project(name='ProjectA')
project2 = Project(name='ProjectB')

session.add_all([user1, user2, project1, project2])
session.commit()

# Додавання зв'язків між користувачами та проектами через асоціаційну таблицю
user1.projects.append(project1)
user1.projects.append(project2)
user2.projects.append(project2)

session.commit()

# Виведення інформації про користувачів та їхні проекти
print("Users:")
for user in session.query(User).all():
    print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}, Projects: {', '.join([project.name for project in user.projects])}")

print("\nProjects:")
for project in session.query(Project).all():
    print(f"Project ID: {project.id}, Name: {project.name}, Users: {', '.join([user.username for user in project.users])}")

# Закриття сесії
session.close()