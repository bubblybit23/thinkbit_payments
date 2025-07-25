import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME")
)

cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM transactions")
print(f"PH Transactions: {cur.fetchone()[0]} records")
cur.close()
conn.close()

#outcome: PH Transactions: 4 records