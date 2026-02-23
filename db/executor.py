# db/executor.py

import psycopg

def execute_sql(sql: str):
    conn = psycopg.connect(
        host="localhost",
        dbname="mydb",
        user="myuser",
        password="123456"
    )

    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        columns = [c[0] for c in cur.description]

    conn.close()
    return columns, rows
