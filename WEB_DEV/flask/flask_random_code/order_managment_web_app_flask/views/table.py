from datetime import datetime

import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, session
import config


# Blueprint
main_table = Blueprint('main_table', __name__)
# Import database connection info
params = config.sql_db
# Import current date
year = datetime.now().year
date_today = datetime.today().strftime('%Y-%m-%d')
# Create headers list
headers = ["COMPANY", "CLIENT", "PHONE NUMBER", "ORDER NAME", "ORDER TERM",
           "STATUS", "COMMENTS", "UPDATED", "", ""]


@main_table.route('/')
def order_table():
    """ MAIN TABLE """

    if 'user' in session:
        # Connect to SQL and fetch data
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute(
            """SELECT id, company, client, phone_number, order_name,
            order_term, status, comments, update_date
            FROM orders 
            ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
        query = cur.fetchall()

        # Create list of data from SQL, enumerate is for table row numbers -> look at table.html
        data = [data_item for data_item in enumerate(query, 1)]
        
        # Clean list from dublicates by using "set"
        show_names = sorted(set([name[4] for name in query
                           if name[4] != "" and name[4] is not None]))

        # Close SQL connection
        con.close()

        return render_template('main_page/table.html', headers=headers, year=year, data=data, show_names=show_names, view_value='main')

    else:
        return redirect(url_for('login_bp.login'))


@main_table.route("/filter/<order_name>")
def filter_table(order_name):
    """ FILTER TABLE """

    order_name_ = None

    if 'user' in session:
        # Connect to SQL and fetch data
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute(
            f"""SELECT id, company, client, phone_number, order_name,
                order_term, status, comments, update_date
                FROM orders
                ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
        query = cur.fetchall()

        # Clean list from dublicates by using "set"
        show_names = sorted(set([name[4] for name in query
                           if name[4] != "" and name[4] is not None]))

        # Fetch filtered table data
        data = []
        for item in show_names:
            if item == order_name:
                order_name_ = order_name
                cur.execute(
                    f"""SELECT id, company, client, phone_number, order_name,
                    order_term, status, comments, update_date
                    FROM orders WHERE order_name = '{order_name_}'
                    ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
                query = cur.fetchall()

                # Create list of all data from SQL
                data = [row for row in enumerate(query, 1)]

        # Close SWL connection
        con.close()

        return render_template('main_page/table.html', headers=headers, year=year, data=data, show_names=show_names, view_value='main')

    else:
        return redirect(url_for('login_bp.login'))


@main_table.route("/sort/<sort_name>")
def sort_table(sort_name):
    """ SORT TABLE """

    sort_name_ = None

    if 'user' in session:
        # Connect to SQL and fetch data
        con = psycopg2.connect(**params)
        cur = con.cursor()
        cur.execute(
            """SELECT id, company, client, phone_number, order_name,
            order_term, status, comments, update_date
            FROM orders
            ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
        query = cur.fetchall()

        # Get headers names from sql for sorting
        headers_sql_ = [i[0] for i in cur.description if i != "id"]
        
        # Add headers to dict
        dict_sort = {headers[i]: headers_sql_[i]
                     for i in range(0, len(headers)-2)}

        # Clean list from dublicates by using "set"
        show_names = sorted(set([name[4] for name in query
                           if name[4] != "" and name[4] is not None]))

        # Fetch filtered table data
        data = []
        for key in dict_sort:
            # print(key)
            if key == sort_name:
                sort_name_ = dict_sort[key]

                cur.execute(
                    f"""SELECT id, company, client, phone_number, order_name,
                        order_term, status, comments, update_date
                        FROM orders
                        ORDER BY {sort_name_} ASC""")
                query = cur.fetchall()

                # Create list of all data from SQL
                data = [row for row in enumerate(query, 1)]

        # Close SWL connection
        con.close()

        return render_template('main_page/table.html', headers=headers, year=year, data=data, show_names=show_names, view_value='main')

    else:
        return redirect(url_for('login_bp.login'))


@main_table.route('/search', methods=['POST'])
def search_table():
    """ SEARCH TABLE """

    if 'user' in session:
        search_form = request.form.get('search')

        if search_form is not None and search_form != "":
            # Connect to SQL and fetch data
            con = psycopg2.connect(**params)
            cur = con.cursor()
            cur.execute(
                """SELECT id, company, client, phone_number, order_name,
                    order_term, status, comments, update_date
                    FROM orders
                    ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""")
            query = cur.fetchall()

            # Clean list from dublicates by using "set"
            show_names = sorted(set([name[4] for name in query
                               if name[4] != "" and name[4] is not None]))

            # Connect to SQL and fetch data
            cur.execute(
                """SELECT id, company, client, phone_number, order_name,
                order_term, status, comments, update_date
                FROM orders 
                WHERE company ILIKE %s 
                OR client ILIKE %s 
                OR phone_number ILIKE %s 
                OR order_name ILIKE %s 
                OR comments ILIKE %s
                ORDER BY status ASC, order_term ASC, order_name ASC, client ASC""",
                ('%' + search_form + '%', '%' + search_form + '%', '%' + search_form + '%', '%' + search_form + '%', '%' + search_form + '%'))

            query = cur.fetchall()
            # Create list of all data from SQL
            data = [row for row in enumerate(query, 1)]

            # Close SQL connection
            con.close()

            return render_template('main_page/table.html', headers=headers, year=year, data=data, show_names=show_names, view_value='main', search_form=search_form)

        else:
            return redirect(url_for('main_table.order_table'))

    else:
        return redirect(url_for('login_bp.login'))
