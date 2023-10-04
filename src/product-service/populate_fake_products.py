from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product
from faker import Faker
import random

# PostgreSQL database configuration
DATABASE_URL = 'postgresql://antonv:password@localhost/exampleapp'
engine = create_engine(DATABASE_URL)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

def generate_fake_product():
    fake = Faker()
    name = fake.word() + ' ' + fake.word()
    description = fake.sentence()
    price = random.randint(10, 1000)  # Generate a random price

    return Product(name=name, description=description, price=price)

if __name__ == '__main__':
    session = DBSession()

    try:
        # Generate 10 fake products and insert into the database
        for _ in range(10):
            fake_product = generate_fake_product()
            session.add(fake_product)
            session.commit()
            print(f"Inserted product: {fake_product.name}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        session.rollback()

    finally:
        session.close()

