from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Create an SQLite database in memory for this example
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

# Define SQLAlchemy models
# Define the Author model
class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Create a one-to-many relationship between Author and Book
    books = relationship("Book", back_populates="author", cascade="all, delete-orphan")

# Define the Book model
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))  # Create a foreign key to link to the Author
    author = relationship("Author", back_populates="books")  # Create a back-reference relationship to Author

# Create the tables in the database
Base.metadata.create_all(engine)

# Insert sample data
Session = sessionmaker(bind=engine)
session = Session()

# Create an Author instance (J.K. Rowling)
author1 = Author(name="J.K. Rowling")
# Create a Book instance (Harry Potter) associated with author1
book1 = Book(title="Harry Potter", author=author1)

# Create another Author instance (George Orwell)
author2 = Author(name="George Orwell")
# Create a Book instance (1984) associated with author2
book2 = Book(title="1984", author=author2)

# Add the Author and Book instances to the session
session.add_all([author1, author2, book1, book2])

# Commit the changes to the database
session.commit()

# Delete author1 and observe the cascade effects
session.delete(author1)
session.commit()

# Query the database to see the results
print("Authors after cascading delete:")
authors = session.query(Author).all()
for author in authors:
    # Print the author's name and the titles of their books
    print(f"Author: {author.name}, Books: {[book.title for book in author.books]}")

# Now, let's update author2's books and see the cascade effect
# Create a new Book instance (Animal Farm) associated with author2
book3 = Book(title="Animal Farm", author=author2)
# Add the new book to the session
session.add(book3)
# Commit the changes to the database
session.commit()

print("\nAuthor2 after adding a book:")
# Query author2 from the database
author2 = session.query(Author).filter_by(name="George Orwell").first()
# Print the author's name and the titles of their books
print(f"Author: {author2.name}, Books: {[book.title for book in author2.books]}")
