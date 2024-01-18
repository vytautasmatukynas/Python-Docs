import psycopg2

import db_conn

uzsakymai_db_params = db_conn.uzsakymai_db
komponentai_db_params = db_conn.komponentai_db
rolikai_db_params = db_conn.rolikai_db
sanaudos_db_params = db_conn.sanaudos_db
stelazas_db_params = db_conn.stelazas_db

# conn = psycopg2.connect(
#     **uzsakymai_db_params
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

# con = psycopg2.connect(
#     **komponentai_db_params
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
#     **rolikai_db_params
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

# con = psycopg2.connect(
#     **sanaudos_db_params
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
#     **stelazas_db_params
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