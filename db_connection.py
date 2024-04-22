from sqlalchemy import create_engine

# Define the database URI
db_uri = "postgresql://rswel:ca19961998@localhost:5432/ratings"

try:
    # Create an engine to connect to the database
    engine = create_engine(db_uri)
    
    # Test the connection by executing a simple query
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        row = result.fetchone()
        if row[0] == 1:
            print("Connected to the database successfully.")
        else:
            print("Error connecting to the database.")
except Exception as e:
    print("Error connecting to the database:", e)
