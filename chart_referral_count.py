import pandas as pd
import matplotlib.pyplot as plt
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database connection parameters
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    database=os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

# Fetch referral data
query = "SELECT referral_datetime, patient_state FROM ereferral"
df = pd.read_sql_query(query, conn)

#print how many rows of data we got from the query

print(df.shape)

# Close the connection
conn.close()

# Prepare the data
df['referral_datetime'] = pd.to_datetime(df['referral_datetime'])
df['month'] = df['referral_datetime'].dt.to_period('M')
grouped = df.groupby(['month', 'patient_state']).size().unstack(fill_value=0)

# Plot
grouped.plot(kind='bar', stacked=True, figsize=(10, 7))
plt.title('Total Number of Referrals by Month')
plt.xlabel('Month')
plt.ylabel('Number of Referrals')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
