# import psycopg2
# import db_conn
# sanaudos_db_params = db_conn.sanaudos_db
#
# con = psycopg2.connect(
#     **sanaudos_db_params
#     )
#
# c = con.cursor()
# c.execute("""SELECT kiekis FROM sanaudos WHERE pavadinimas = 'HABASIT'""")
# query = c.fetchall()
#
# lista = []
#
# for row_date in query:
#     for column_number, data in enumerate(row_date):
#         lista.append(int(data))
#         print(data)
#
# print(sum(lista))
import psycopg2

import db_conn
sanaudos_db_params = db_conn.sanaudos_db

con = psycopg2.connect(**sanaudos_db_params)

pav_list = ['HABASIT', 'PROFILIAI', 'UZDENGIMAI', 'GALINUKAS', 'PRILAIKANTIS', 'SKRIEMULYS', 'SKRIEMULIO ASIS']
for pav in pav_list:
    # print(pav)
    c = con.cursor()

    c.execute(f"""SELECT pavadinimas, kiekis FROM sanaudos WHERE pavadinimas = '{pav}'""")
    # c1.execute(f"""SELECT kiekis FROM sanaudos WHERE pavadinimas = 'PROFILIAI' AND metai = '{year}'""")
    # c2.execute(f"""SELECT kiekis FROM sanaudos WHERE pavadinimas = 'UZDENGIMAI' AND metai = '{year}'""")
    # c3.execute(f"""SELECT kiekis FROM sanaudos WHERE pavadinimas = 'GALINUKAS' AND metai = '{year}'""")
    # c4.execute(f"""SELECT kiekis FROM sanaudos WHERE pavadinimas = 'PRILAIKANTIS' AND metai = '{year}'""")
    # c5.execute(f"""SELECT kiekis FROM sanaudos WHERE pavadinimas = 'SKRIEMULYS' AND metai = '{year}'""")
    # c6.execute(f"""SELECT kiekis FROM sanaudos WHERE pavadinimas = 'SKRIEMULIO ASIS' AND metai = '{year}'""")

    # query, query1, query2, query3, query4, query5, query6 = (c.fetchall(), c1.fetchall(), c2.fetchall(),
    #                                                          c3.fetchall(), c4.fetchall(), c5.fetchall(),
    #                                                          c6.fetchall())
    query = c.fetchall()
    for row_date in query:
        for column_number, data in enumerate(row_date):
            lista = []
            lista.append(data)
            print(lista[0])
            listb = []
            listb.append(lista[0])
            print(listb)

    c.close()

