import os
import psycopg2
from dotenv import load_dotenv

# Define a class to represent a referral
class Referral:
    def __init__(
        self, referral_id, e_referral_id, referral_datetime, clinician_name,
        clinician_contact_details, healthcare_provider_number, practice_name,
        practice_contact_details, secure_messaging_provider, secure_messaging_endpoint,
        patient_first_name, patient_last_name, patient_contact_details,
        patient_alternate_contact_name, patient_alternate_contact_details,
        target_organisation_name, target_faculty, referral_reason, medication_history,
        comorbidity, patient_dob, medicare_number, medicare_expiry, atsi_code,
        primary_language_code, additional_info, patient_full_address, patient_email,
        patient_postcode, patient_state
    ):
        self.referral_id = referral_id
        self.e_referral_id = e_referral_id
        self.referral_datetime = referral_datetime
        self.clinician_name = clinician_name
        self.clinician_contact_details = clinician_contact_details
        self.healthcare_provider_number = healthcare_provider_number
        self.practice_name = practice_name
        self.practice_contact_details = practice_contact_details
        self.secure_messaging_provider = secure_messaging_provider
        self.secure_messaging_endpoint = secure_messaging_endpoint
        self.patient_first_name = patient_first_name
        self.patient_last_name = patient_last_name
        self.patient_contact_details = patient_contact_details
        self.patient_alternate_contact_name = patient_alternate_contact_name
        self.patient_alternate_contact_details = patient_alternate_contact_details
        self.target_organisation_name = target_organisation_name
        self.target_faculty = target_faculty
        self.referral_reason = referral_reason
        self.medication_history = medication_history
        self.comorbidity = comorbidity
        self.patient_dob = patient_dob
        self.medicare_number = medicare_number
        self.medicare_expiry = medicare_expiry
        self.atsi_code = atsi_code
        self.primary_language_code = primary_language_code
        self.additional_info = additional_info
        self.patient_full_address = patient_full_address
        self.patient_email = patient_email
        self.patient_postcode = patient_postcode
        self.patient_state = patient_state

    def __str__(self):
        return (
            f"Referral ID: {self.referral_id}\n"
            f"E-Referral ID: {self.e_referral_id}\n"
            f"Referral Datetime: {self.referral_datetime}\n"
            f"Clinician Name: {self.clinician_name}\n"
            f"Clinician Contact Details: {self.clinician_contact_details}\n"
            f"Healthcare Provider Number: {self.healthcare_provider_number}\n"
            f"Practice Name: {self.practice_name}\n"
            # ... add other fields here in the same format
        )

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
rows = cursor.fetchall()

# Close the cursor and connection to the server
cursor.close()
conn.close()

# Process each row into a Referral instance and print
for row in rows:
    referral = Referral(*row)  # Unpack all the row fields into the Referral constructor
    print(referral)  # Print the Referral instance using the __str__ method for presentable output
