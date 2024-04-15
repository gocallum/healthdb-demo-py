import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Connect to the database
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

# Fetch referral data by ATSI status
query = "SELECT referral_status, COUNT(*) AS count FROM ereferral GROUP BY referral_status"
df = pd.read_sql_query(query, conn)

df['percentage'] = (df['count'] / df['count'].sum()) * 100
print(df)
# Close the connection
conn.close()

