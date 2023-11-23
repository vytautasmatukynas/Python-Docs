from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import select, func

# Create an SQLite database in memory for this example
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()

# Define SQLAlchemy model
class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    department = Column(String)

# Create the table
Base.metadata.create_all(engine)

# Insert sample data
Session = sessionmaker(bind=engine)
session = Session()

alice = Employee(name="Alice", department="HR")
bob = Employee(name="Bob", department="IT")
charlie = Employee(name="Charlie", department="IT")
dave = Employee(name="Dave", department="HR")
eve = Employee(name="Eve", department="IT")

session.add_all([alice, bob, charlie, dave, eve])
session.commit()

# Perform a group_by query
employees = Employee.__table__
stmt = select([employees.c.department, func.count().label('count')]).group_by(employees.c.department)

result = session.execute(stmt)
for row in result:
    print(f"Department: {row.department}, Count: {row.count}")
