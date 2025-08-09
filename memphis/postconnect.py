import psycopg2

try:
    conn = psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="postgres_password",
        host="127.0.0.1",
        port=5432
    )
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Postgres versiyası:", version[0])
    cur.close()
    conn.close()
except Exception as e:
    print("Bağlantı xətası:", e)
