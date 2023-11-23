import psycopg2

""" Sample for connection to PostgreSQL DB"""

params = psycopg2.connect(
    host='your_host',
    database='your_database',
    user='your_user',
    password='your_password',
    port='5432'
)

conn = psycopg2.connect(**params)

cur = conn.cursor()

cur.execute("""SELECT * FROM sampleTable ORDER BY id""")

query = cur.fetchall()

conn.close()
