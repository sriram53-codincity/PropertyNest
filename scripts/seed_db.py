import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("PG_DATABASE"), 
    user=os.getenv("PG_USER"), 
    password=os.getenv("PG_PASSWORD"), 
    host=os.getenv("PG_HOST")
)
conn.autocommit = True
cur = conn.cursor()

# Insert a user
cur.execute("""
    INSERT INTO property_nest.users (full_name, email, password, is_active) 
    VALUES ('Srimathi Maran', 'sri@test.com', 'hashed_pwd', true) 
    RETURNING id;
""")
user_id = cur.fetchone()[0]

# Insert user roles
cur.execute("INSERT INTO property_nest.user_roles (user_id, role) VALUES (%s, 'BUYER')", (user_id,))
cur.execute("INSERT INTO property_nest.user_roles (user_id, role) VALUES (%s, 'SELLER')", (user_id,))

# Insert some properties with integer IDs
properties = [
    ('Luxury Villa', 'Los Angeles', 'HOUSE', 5, 4, 15000),
    ('Cozy Apartment', 'New York', 'APARTMENT', 2, 1, 3000),
    ('Downtown Studio', 'Chicago', 'APARTMENT', 1, 1, 1500)
]

for p in properties:
    cur.execute("""
        INSERT INTO property_nest.properties (owner_id, title, city, property_type, bedrooms, bathrooms, monthly_rent, status, is_available) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'PUBLISHED', true)
    """, (user_id, p[0], p[1], p[2], p[3], p[4], p[5]))

conn.commit()
print("Successfully added 1 User and 3 Properties to the database!")
