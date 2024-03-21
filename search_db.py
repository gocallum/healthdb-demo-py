import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database credentials from the .env file
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Establish a connection to the database
conn = psycopg2.connect(
    host=POSTGRES_HOST,
    database=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD
)

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Execute the SQL command
cursor.execute("SELECT * FROM ereferral")

# Fetch all rows from the last executed statement
records = cursor.fetchall()

# Print the records
for record in records:
    print(record)

# Close the cursor and connection to the server
cursor.close()
conn.close()
