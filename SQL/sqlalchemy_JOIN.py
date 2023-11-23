from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select

# Create a PostgreSQL database connection
# Replace 'username', 'password', 'localhost', and 'mydatabase' with your
# PostgreSQL database credentials and information.
engine = create_engine('postgresql://username:password@localhost/mydatabase', echo=True)

# Create a base class for declarative models
Base = declarative_base()


# Define SQLAlchemy models for the Department and Employee tables
class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    department_id = Column(Integer)


# Create the database tables based on the defined models
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert sample data into the tables
hr = Department(name="HR")
it = Department(name="IT")
alice = Employee(name="Alice", department_id=1)
bob = Employee(name="Bob", department_id=2)
charlie = Employee(name="Charlie", department_id=1)
session.add_all([hr, it, alice, bob, charlie])
session.commit()

# Define the SQLAlchemy tables for the Department and Employee models
departments = Department.__table__
employees = Employee.__table__

# Perform an INNER JOIN between the Department and Employee tables
inner_join_stmt = select([departments.c.name, employees.c.name]).select_from(
    departments.join(employees, departments.c.id == employees.c.department_id))
print("INNER JOIN:")
result = session.execute(inner_join_stmt)
for row in result:
    print(row)

# Perform a LEFT JOIN between the Department and Employee tables
left_join_stmt = select([departments.c.name, employees.c.name]).select_from(
    departments.outerjoin(employees, departments.c.id == employees.c.department_id))
print("\nLEFT JOIN:")
result = session.execute(left_join_stmt)
for row in result:
    print(row)

# Perform a RIGHT JOIN between the Department and Employee tables
right_join_stmt = select([departments.c.name, employees.c.name]).select_from(
    employees.outerjoin(departments, employees.c.department_id == departments.c.id))
print("\nRIGHT JOIN:")
result = session.execute(right_join_stmt)
for row in result:
    print(row)

# Simulate a FULL JOIN using a UNION of LEFT JOIN and RIGHT JOIN
full_join_stmt = left_join_stmt.union(right_join_stmt)
print("\nFULL JOIN (simulated):")
result = session.execute(full_join_stmt)
for row in result:
    print(row)
