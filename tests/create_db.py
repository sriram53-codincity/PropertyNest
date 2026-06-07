import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="9715907196",
    host="localhost",
    port="5432"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

try:
    cur.execute("CREATE DATABASE homelease_test;")
    print("Database homelease_test created successfully.")
except psycopg2.errors.DuplicateDatabase:
    print("Database homelease_test already exists.")

cur.close()
conn.close()
