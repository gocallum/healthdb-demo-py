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
query = "SELECT atsi_code, COUNT(*) AS count FROM ereferral GROUP BY atsi_code"
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Calculate percentage
df['percentage'] = (df['count'] / df['count'].sum()) * 100

# Plot pie chart
plt.figure(figsize=(8, 8))
plt.pie(df['percentage'], labels=df['atsi_code'], autopct='%1.1f%%', startangle=140)
plt.title('Distribution of Referrals by ATSI Status')
plt.show()
