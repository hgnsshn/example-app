from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User
from faker import Faker
import random

# PostgreSQL database configuration
DATABASE_URL = 'postgresql://antonv:password@localhost/exampleapp'
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

def generate_fake_user():
    fake = Faker()
    username = fake.user_name()
    password = fake.password()
    email = fake.email()
    full_name = fake.name()

    return User(username=username, password=password, email=email, full_name=full_name)

if __name__ == '__main__':
    session = DBSession()

    try:
        # Generate 10 fake users and insert into the database
        for _ in range(10):
            fake_user = generate_fake_user()
            session.add(fake_user)
            session.commit()
            print(f"Inserted user: {fake_user.username}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()

    finally:
        session.close()

