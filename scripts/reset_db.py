import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

print("Dropping property_nest schema to wipe database...")
conn = psycopg2.connect(
    dbname=os.getenv("PG_DATABASE"), 
    user=os.getenv("PG_USER"), 
    password=os.getenv("PG_PASSWORD"), 
    host=os.getenv("PG_HOST")
)
conn.autocommit = True
cur = conn.cursor()
cur.execute("DROP SCHEMA property_nest CASCADE;")
cur.execute("CREATE SCHEMA property_nest;")
cur.execute("GRANT ALL ON SCHEMA property_nest TO postgres;")
cur.execute("GRANT ALL ON SCHEMA property_nest TO public;")
print("Postgres wiped successfully.")
