import psycopg2
import pandas as pd
import numpy as np
from datetime import timedelta
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, EasterMonday, GoodFriday
from dotenv import load_dotenv
import os

# Define an Australian Holiday Calendar
class AustralianHolidayCalendar(AbstractHolidayCalendar):
    rules = [
        Holiday("New Year's Day", month=1, day=1, observance=nearest_workday),
        Holiday("Australia Day", month=1, day=26, observance=nearest_workday),
        GoodFriday,
        EasterMonday,
        Holiday("Anzac Day", month=4, day=25),
        Holiday("Queen's Birthday", month=6, day=1, offset=pd.DateOffset(weekday=pd.offsets.WeekOfMonth(week=1, weekday=0))),
        Holiday("Labour Day (WA)", month=3, day=1, offset=pd.DateOffset(weekday=pd.offsets.WeekOfMonth(week=0, weekday=0))),
        Holiday("Labour Day (VIC & TAS)", month=3, day=1, offset=pd.DateOffset(weekday=pd.offsets.WeekOfMonth(week=1, weekday=0))),
        Holiday("Labour Day (NSW, ACT, SA)", month=10, day=1, offset=pd.DateOffset(weekday=pd.offsets.WeekOfMonth(week=0, weekday=0))),
        Holiday("Labour Day (QLD)", month=5, day=1, offset=pd.DateOffset(weekday=pd.offsets.WeekOfMonth(week=1, weekday=0))),
        Holiday("Christmas Day", month=12, day=25, observance=nearest_workday),
        Holiday("Boxing Day", month=12, day=26, observance=nearest_workday),
    ]



# Load environment variables
load_dotenv()

# Connect to the database
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    dbname=os.getenv("POSTGRES_DATABASE"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD")
)

# Define a cursor to use with your SQL statements
cursor = conn.cursor()

# Fetch referral data
query = "SELECT referral_id, referral_datetime, referral_status, referral_accepted_rejected_date FROM ereferral"
df = pd.read_sql_query(query, conn)

# Set seed for reproducibility
np.random.seed(42)

# Determine the new statuses
# 60% accepted, 20-30% rejected, 10% processing
statuses = np.random.choice([1, 2, 0], size=len(df), p=[0.6, 0.25, 0.15])
df['new_status'] = statuses

# Function to calculate accepted/rejected date within business rules
def calculate_decision_date(row):
    start_date = pd.Timestamp(row['referral_datetime'])
    cal = AustralianHolidayCalendar()
    holidays = cal.holidays(start=start_date, end=start_date + pd.DateOffset(days=10))

    if np.random.rand() <= 0.6:  # 60% within 1 business day
        days_added = np.random.choice([0, 1])
    elif np.random.rand() <= 0.9:  # Next 30% within 3 days
        days_added = np.random.choice([2, 3])
    else:  # Rest within 5 days
        days_added = np.random.choice([4, 5])

    # Calculate a business day date
    result_date = start_date + pd.DateOffset(days=days_added)
    while result_date.weekday() >= 5 or result_date in holidays:
        result_date += pd.DateOffset(days=1)
    return result_date

# Apply function to calculate the new accepted/rejected dates
df['new_accepted_rejected_date'] = df.apply(calculate_decision_date, axis=1)

# Update the database
update_query = """
    UPDATE ereferral SET
    referral_status = %s,
    referral_accepted_rejected_date = %s
    WHERE referral_id = %s
"""
for _, row in df.iterrows():
    cursor.execute(update_query, (row['new_status'], row['new_accepted_rejected_date'], row['referral_id']))

# Commit changes
conn.commit()

# Close the connection
cursor.close()
conn.close()
