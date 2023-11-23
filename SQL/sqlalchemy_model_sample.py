from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# import psycopg2
#
# SQL SAMPLE <---
# conn = psycopg2.connect(
#     host='your_host',
#     database='your_database',
#     user='your_user',
#     password='your_password',
#     port='5432'
# )
#
# cur = conn.cursor()
#
# create_author_table = """
# CREATE TABLE IF NOT EXISTS authors (
#     id SERIAL PRIMARY KEY,
#     name VARCHAR(255) NOT NULL
# )
# """
#
# create_book_table = """
# CREATE TABLE IF NOT EXISTS books (
#     id SERIAL PRIMARY KEY,
#     title VARCHAR(255) NOT NULL,
#     author_id INT REFERENCES authors(id)
# )
# """
#
# cur.execute(create_author_table)
# cur.execute(create_book_table)
#
# conn.commit()
#
# conn.close()

""" SQLALchemy Model sample """
# Create the SQLAlchemy engine
engine = create_engine('sqlite:///library.db', echo=True)  # Using SQLite for this example

# Create a base class for declarative models
Base = declarative_base()


# Define the Author model
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    # Define a one-to-many relationship with Book
    books = relationship('Book', back_populates='author')


# Define the Book model
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))

    # Define a many-to-one relationship with Author
    author = relationship('Author', back_populates='books')


# Create the tables in the database
Base.metadata.create_all(engine)
