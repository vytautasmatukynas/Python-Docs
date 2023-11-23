from sqlalchemy import create_engine, text

# Define the connection string
connection_string = "postgresql://user:password@host:port/database"

# Create an SQLAlchemy engine
engine = create_engine(connection_string)

# Create a SQLAlchemy connection
connection = engine.connect()

# Define the SQL query
query = text("SELECT * FROM sampleTable ORDER BY id")

# Execute the query and fetch the results
result = connection.execute(query).fetchall()

# Close the connection
connection.close()

