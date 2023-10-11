import psycopg2
from faker import Faker
import random

# PostgreSQL database configuration
DATABASE_URL = 'postgresql://exampleuser:password@localhost:5432/exampleapp'

# Connect to the PostgreSQL database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

fake = Faker()

# Generate and insert fake orders
for _ in range(10):
    product_id = random.randint(1, 3)  # Assuming products have IDs from 1 to 3
    user_id = random.randint(1, 10)  # Assuming users have IDs from 1 to 10
    quantity = random.randint(1, 10)

    cur.execute("INSERT INTO orders (product_id, user_id, quantity) VALUES (%s, %s, %s)",
                (product_id, user_id, quantity))

conn.commit()
cur.close()
conn.close()

print("Fake orders inserted successfully.")

