import psycopg2
from faker import Faker
import random

from config import sql_db


params = sql_db

# Main DB Table
conn = psycopg2.connect(**params)
cur = conn.cursor()
cur.execute(("""CREATE TABLE IF NOT EXISTS orders (
            ID INT GENERATED ALWAYS AS IDENTITY,
            company VARCHAR(100),
            client VARCHAR(100),
            phonenumber VARCHAR(50),
            ordername VARCHAR(100),
            term VARCHAR(50),
            status VARCHAR(50),
            comments TEXT,
            folderdir VARCHAR(255),
            filename VARCHAR(150),
            updatedate VARCHAR(50),
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
            phonenumber VARCHAR(50),
            ordername VARCHAR(50)
            )
            """))
conn.commit()
conn.close()

# Users DB Table
conn = psycopg2.connect(**params)
cur = conn.cursor()
cur.execute(("""CREATE TABLE IF NOT EXISTS users_orders (
            ID INT GENERATED ALWAYS AS IDENTITY,
            username TEXT,
            password TEXT,
            privs TEXT
            )
            """))
conn.commit()
conn.close()

###############################################################
# Populate DB with fake data for testing
fake = Faker()
# Generate a fake name
fake_name = fake.name()
# Generate a fake phone number
fake_phone_number = fake.phone_number()
# Generate a fake date
fake_date = fake.date()
# Generate a fake email
fake_email = fake.email()
# Generate a fake text
fake_text = fake.text(max_nb_chars=50)
# Generate a fake file name
fake_file_name = fake.file_name(category=None, extension=None)

status = ['IN PROCESS', 'FINISHED']
date = ['-', '+', fake_date]

# insert 5 rows of fake data to db
company = random.choice(fake_name)
client = random.choice(fake_email)
phone = random.choice(fake_phone_number)
name = random.choice(fake_name)
term = random.choice(date)
status = random.choice(status)
comments = random.choice(fake_text)
folder = "D:/" + random.choice(fake_file_name)
file = random.choice(fake_file_name)
update_date = random.choice(fake_date)

conn = psycopg2.connect(**params)
cur = conn.cursor()

for _ in range(50):
    cur.execute('''INSERT INTO orders (company, client, phonenumber, ordername,
        term, status, comments, folderdir, filename, updatedate) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                (company, client, phone, name,
                    term, status, comments, folder, file, update_date,))
    
conn.commit()
conn.close()