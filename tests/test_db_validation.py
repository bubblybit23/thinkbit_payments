import psycopg2
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="module")
def db_conn():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME")
    )
    yield conn
    conn.close()

def test_gcash_success_rate(db_conn):
    with db_conn.cursor() as cur:
        cur.execute("""
WITH num_gcash AS (
    SELECT id
    FROM transactions 
    WHERE payment_method='GCASH' AND status='COMPLETED'
)

SELECT 
	COUNT(n.id) AS complete,
	COUNT(*) AS total
FROM transactions t
LEFT JOIN num_gcash n
ON t.id = n.id
WHERE payment_method = 'GCASH'
        """)
        completed, total = cur.fetchone()
        #output 2/4 since we have another input from flask
        assert completed / total > 0.5

def test_php_currency(db_conn):

    with db_conn.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM transactions WHERE currency != 'PHP'")
        assert cur.fetchone()[0] == 0

def test_high_value_transactions(db_conn):
   
    with db_conn.cursor() as cur:
        cur.execute("SELECT id FROM transactions WHERE amount > 10000")
        assert cur.rowcount == 0