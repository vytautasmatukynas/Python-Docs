import psycopg2

from config import sql_db

params = sql_db

conn = psycopg2.connect(**params)
cur = conn.cursor()

cur.execute(("""CREATE TABLE IF NOT EXISTS orders (
            ID INT GENERATED ALWAYS AS IDENTITY,
            company VARCHAR(100),
            client VARCHAR(100),
            phone_number VARCHAR(50),
            order_name VARCHAR(100),
            order_term VARCHAR(50),
            status VARCHAR(50),
            comments TEXT,
            order_folder VARCHAR(255),
            order_file VARCHAR(150),
            update_date VARCHAR(50),
            filename VARCHAR(150),
            photo BYTEA,
            filetype VARCHAR(30),
            filedir VARCHAR(255)
            )
            """))

conn.commit()

conn.close()

# ComboBox DB Table
conn = psycopg2.connect(**params)

cur = conn.cursor()

cur.execute(("""CREATE TABLE IF NOT EXISTS combo_orders (
            ID INT GENERATED ALWAYS AS IDENTITY,
            company VARCHAR(50),
            client VARCHAR(50),
            phone_number VARCHAR(50),
            order_name VARCHAR(50)
            )
            """))

conn.commit()
conn.close()


# conn = psycopg2.connect(**params)
# cur = conn.cursor()

# cur.execute(("""CREATE TABLE IF NOT EXISTS atkrovimai (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             projektas TEXT,
#             pavarinimas TEXT,
#             sarasas TEXT,
#             komentarai TEXT,
#             filename TEXT,
#             photo BYTEA NOT NULL,
#             filetype TEXT,
#             filedir TEXT
#             )
#             """))
#
# conn.commit()

# Orders DB Table
#
# conn.close()
#
# conn = psycopg2.connect(
#     **params
# )
# cur = conn.cursor()
#
# cur.execute(("""CREATE TABLE IF NOT EXISTS atkrovimai (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             pavadinimas TEXT,
#             bendras TEXT,
#             paleciu TEXT,
#             komentarai TEXT,
#             update_date TEXT
#             )
#             """))
#
# conn.commit()
# conn.close()
#
# conn = psycopg2.connect(
#     **params
# )
# cur = conn.cursor()
#
# cur.execute(("""CREATE TABLE IF NOT EXISTS pavaros (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             pavadinimas TEXT,
#             gamintojas TEXT,
#             tipas TEXT,
#             galia TEXT,
#             apsisukimai TEXT,
#             momentas TEXT,
#             tvirtinimas TEXT,
#             kiekis TEXT,
#             komentarai TEXT,
#             update_date TEXT
#             )
#             """))
#
# conn.commit()
# conn.close()
#
# conn = psycopg2.connect(
#     **params
# )
# cur = conn.cursor()
#
# cur.execute(("""CREATE TABLE IF NOT EXISTS combo (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             uzsakymai_imone TEXT,
#             uzsakymai_konstruktorius TEXT,
#             uzsakymai_projektas TEXT,
#             uzsakymai_pavadinimas TEXT
#             )
#             """))
#
# conn.commit()
# conn.close()
#
# conn = psycopg2.connect(
#     **params
# )
# cur = conn.cursor()
#
# cur.execute(("""CREATE TABLE IF NOT EXISTS uzsakymai (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             IMONE TEXT,
#             KONSTRUKTORIUS TEXT,
#             PROJEKTAS TEXT,
#             PAV_UZSAKYMAI TEXT,
#             TERMINAS TEXT,
#             STATUSAS TEXT,
#             KOMENTARAI TEXT,
#             BREZINIAI TEXT,
#             SARASAS TEXT
#             )
#             """))
#
# conn.commit()
# conn.close()
#
# con = psycopg2.connect(
#     **params
# )
#
# c = con.cursor()
#
# c.execute("""CREATE TABLE IF NOT EXISTS komponentai (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             PAVADINIMAS TEXT,
#             VIETA TEXT,
#             KIEKIS TEXT,
#             MAT_PAV TEXT,
#             KOMENTARAS TEXT,
#             NUOTRAUKA TEXT
#             )
#             """)
#
# con.commit()
#
# conn = psycopg2.connect(
#     **params
# )
# cur = conn.cursor()
#
# cur.execute(("""CREATE TABLE IF NOT EXISTS rolikai (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             PAVADINIMAS TEXT,
#             ILGIS TEXT,
#             KIEKIS TEXT,
#             VIETA TEXT,
#             TVIRTINIMAS TEXT,
#             TIPAS TEXT,
#             KOMENTARAI TEXT
#             )
#             """))
#
# conn.commit()
#
# con = psycopg2.connect(
#     **params
# )
#
# c = con.cursor()
#
# c.execute("""CREATE TABLE IF NOT EXISTS sanaudos (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             PAVADINIMAS TEXT,
#             PROJEKTAS TEXT,
#             KIEKIS TEXT,
#             MAT_VNT TEXT,
#             KOMENTARAS TEXT,
#             METAI TEXT
#             )
#             """)
#
# con.commit()
#
# conn = psycopg2.connect(
#     **params
# )
# cur = conn.cursor()
#
# cur.execute(("""CREATE TABLE IF NOT EXISTS stelazas (
#             ID INT GENERATED ALWAYS AS IDENTITY,
#             PAVADINIMAS TEXT,
#             PROJEKTAS TEXT,
#             SANDELIS TEXT,
#             VIETA TEXT,
#             KOMENTARAI TEXT
#             )
#             """))
#
# conn.commit()