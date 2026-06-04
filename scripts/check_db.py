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
print("Connected to:", conn.get_dsn_parameters())
cur = conn.cursor()
cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'property_nest'
""")
tables = cur.fetchall()
print(f"TABLES in property_nest schema: {tables}")

for t in tables:
    table_name = t[0]
    cur.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cur.fetchone()[0]
    print(f"Table {table_name} has {count} rows.")
