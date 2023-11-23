import pandas as pd
import psycopg2

import config

params = config.sql_db

con = psycopg2.connect(
    **params
)

cur = con.cursor()
cur.execute("""SELECT col_1, col_2, col_3, col_4, col_5, col_6 ORDER BY col_1 ASC,
konfig ASC""")
query = cur.fetchall()

df = pd.DataFrame(query,
                  columns=['col_1', 'col_2', 'col_3', 'col_4', 'col_5', 'col_6'])
print(df)

df.to_excel("output.xlsx", sheet_name='Sheet_name_1', index=False)
df.to_csv('output.csv', index=False)
