from datetime import datetime

import psycopg2
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import config


# Blueprint
edit_table = Blueprint("edit_table", __name__)
# Import DB conn
params = config.sql_db
# Import current date
year = datetime.now().year
date_today = datetime.today().strftime('%Y-%m-%d')
# name for "label" "id" "name". Look at add.html for loop
label_names = ['Company', 'Client', 'Phone Number',
               'Order Name', 'Order Term', 'Status', 'Comments']


@edit_table.route('/add_new', methods=['GET', 'POST'])
def add_order():
    """ ADD NEW RECORD FORM """

    if 'user' in session:
        # if methods is POST get all data from FORM and add it to SQL. Update_date doesn't have request.form,
        # it just auto fills cell with current date.
        if request.method == 'POST':
            company = request.form.get('Company')
            client = request.form.get('Client')
            phone_number = request.form.get('Phone Number')
            order_name = request.form.get('Order Name')
            order_term = request.form.get('Order Term')
            status = request.form.get('Status')
            comments = request.form.get('Comments')
            update_date = f'{date_today}'

            con = psycopg2.connect(**params)
            cur = con.cursor()
            cur.execute('''INSERT INTO orders (company, client, phone_number, order_name,
                order_term, status, comments, update_date) VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s)''',
                        (company, client, phone_number, order_name,
                         order_term, status, comments, update_date,))
            con.commit()
            con.close()

            # if everything is ok, then you will be redirected to main page with table
            return redirect(url_for('main_table.order_table'))

        return render_template('edit_pages/add.html', label_names=label_names, year=year, date_today=date_today, view_value='form')

    else:
        return redirect(url_for('login_bp.login'))


@edit_table.route('/update_order/<int:row_id>', methods=['GET', 'POST'])
def update_order(row_id):
    """ UPDATE RECORD FORM """

    if 'user' in session:
        # if methods is POST get all data from FORM and add it to SQL.
        # if method is GET, gets all data from SQL and fills form with that data,
        # look at html file update.html
        # Update_date doesn't have request.form, it just auto fills cell with current date.
        row_id_ = None

        if request.method == 'POST':
            row_id_ = row_id

            company = request.form.get('Company')
            client = request.form.get('Client')
            phone_number = request.form.get('Phone Number')
            order_name = request.form.get('Order Name')
            order_term = request.form.get('Order Term')
            status = request.form.get('Status')
            comments = request.form.get('Comments')
            update_date = f'{date_today}'

            con = psycopg2.connect(**params)
            cur = con.cursor()
            cur.execute('''UPDATE orders SET company = %s, client = %s, phone_number = %s, order_name = %s, 
                        order_term = %s, status = %s, comments = %s, update_date = %s WHERE id = %s''',
                        (company, client, phone_number, order_name,
                         order_term, status, comments, update_date, row_id_))
            con.commit()
            con.close()

            # if everything is ok, then you will be redirected to main page with table
            return redirect(url_for('main_table.order_table'))

        if request.method == "GET":
            row_id_ = row_id

            con = psycopg2.connect(**params)
            cur = con.cursor()
            cur.execute(
                f"""SELECT * FROM orders WHERE ID=%s""", (row_id_,))
            order_items = cur.fetchone()
            con.close()

            # create dict with data to fill form
            order_data_dict = {label_names[i]: order_items[i+1]
                               for i in range(0, len(label_names))}

        return render_template('edit_pages/update.html', label_names=label_names, year=year, date_today=date_today,
                               order_data_dict=order_data_dict, order_items=order_items, view_value='form')

    else:
        return redirect(url_for('login_bp.login'))


@edit_table.route('/delete/<int:row_id>', methods=['GET', 'POST'])
def delete_order(row_id):
    if 'user' in session:
        """ DELETE RECORD """

        row_id_ = None

        if request.method == "POST":
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("DELETE FROM orders WHERE id = %s", (row_id,))
            conn.commit()
            conn.close()

            flash(f"Order was deleted.")

            return redirect(url_for('main_table.order_table'))

        elif request.method == "GET":
            row_id_ = row_id

        return render_template('edit_pages/delete.html', row_id=row_id_, year=year, view_value='form')

    else:
        return redirect(url_for('login_bp.login'))
