from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

# Create an SQLite database in memory for this example
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

# Define SQLAlchemy model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

# Create the table
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

try:
    # Begin a transaction
    session.begin()

    # Perform database operations
    user1 = User(name="Alice")
    user2 = User(name="Bob")
    user3 = User(name="Alice")  # Duplicate name, should raise IntegrityError

    session.add_all([user1, user2, user3])
    session.commit()

except IntegrityError as e:
    # Handle the IntegrityError (e.g., duplicate entry)
    print(f"IntegrityError: {e}")
    session.rollback()  # Roll back the transaction due to the error

except Exception as e:
    # Handle other exceptions
    print(f"An error occurred: {e}")
    session.rollback()  # Roll back the transaction due to the error

finally:
    # Close the session
    session.close()

# Query the database to check the results
session = Session()
users = session.query(User).all()

print("Users in the database:")
for user in users:
    print(f"ID: {user.id}, Name: {user.name}")
