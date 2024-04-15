from faker import Faker
import random
from psycopg2 import extras  # This is the missing import
import psycopg2
import os
from lib.common_health import generate_australian_gp_name, get_target_organisation_name
from lib.common_health import generate_healthcare_concern
from lib.common_health import generate_comorbidity
from pandas.tseries.offsets import BDay


from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database credentials from the .env file
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

# Set Faker to use the Australian locale for more localized data
fake = Faker('en_AU')


def choose_state():
    # weights for NSW, VIC, QLD respectively
    return random.choices(['NSW', 'VIC', 'QLD'], weights=[0.5, 0.35, 0.15], k=1)[0]

# Function to generate a business date based on a start date

def generate_business_date(start_date):
    if random.random() < 0.70:  # 70% within 1 business day
        days = 1
    elif random.random() < 0.95:  # 25% within 2 business days
        days = 2
    else:  # 5% within 3-4 business days
        days = random.choice([3, 4])
    return start_date + BDay(days)

# Function to choose a status for the referral
# 0 is pending, 1 is accepted, 2 is rejected
def choose_status():
    return random.choices([1, 2, 0], weights=[0.80, 0.15, 0.05], k=1)[0]

def parse_address(address):
    """
    Parses the given address string to extract the state and postcode.
    Assumes the format "Street Address, State, Postcode".
    """
    parts = address.split(',')
    if len(parts) >= 3:
        state = parts[-2].strip()
        postcode = parts[-1].strip()
        return state, postcode
    return None, None




def generate_ereferral_data():
    # Randomly choose an Australian state for consistency in GP name and patient address
    # states = ['NSW', 'VIC', 'QLD']
    chosen_state = choose_state()
    referral_date = fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None)

    referral_status = choose_status()
    if referral_status == 0:
        referral_accepted_rejected_date = None
    else:
        # Ensure the date_time_between includes only business days within the specified range
        referral_accepted_rejected_date = generate_business_date(referral_date)

    # Predefined list of healthcare facilities, including an empty string for blank cases
    healthcare_facilities = [
        "Cardiology",
        "Neurology",
        "Orthopedics",
        "Pediatrics",
        "Oncology",
        "Radiology",
        "Emergency Medicine",
        "",  # Represents a blank entry
    ]


    return {
        'e_referral_id': fake.uuid4(),
        'referral_datetime': referral_date,
        'clinician_name': fake.name(),
        'clinician_contact_details': fake.phone_number(),
        'healthcare_provider_number': fake.bothify(text='????#####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'practice_name': generate_australian_gp_name(),
        'practice_contact_details': fake.phone_number(),
        'secure_messaging_provider': random.choice(['HealthLink', 'Argus', 'ReferralNet', 'Medical Objects']),
        'secure_messaging_endpoint': fake.bothify(text='########'), # Generates an 8-digit alphanumeric code
        'patient_first_name': fake.first_name(),
        'patient_last_name': fake.last_name(),
        'patient_contact_details': fake.phone_number(),
        'patient_alternate_contact_name': fake.name(),
        'patient_alternate_contact_details': fake.phone_number(),
        'target_organisation_name': get_target_organisation_name(),
        'target_faculty': random.choice(healthcare_facilities),  # Select from the list, including potentially blank
        'referral_reason': generate_healthcare_concern(),
        'medication_history': fake.text(max_nb_chars=200),
        'comorbidity': generate_comorbidity(),
        'patient_dob': fake.date_of_birth(minimum_age=5, maximum_age=115),
        'medicare_number': fake.bothify(text='#### #### ##'),  # Adjusted to fit the Medicare format
        'medicare_expiry': fake.date_this_decade(before_today=True, after_today=False),
        'atsi_code': random.choice([1, 2, 3, 4, 9]),
        'primary_language_code': random.randint(1, 100),
        'additional_info': fake.text(max_nb_chars=200),
        'patient_full_address': fake.address(),
        'patient_email': fake.email(),
        'patient_postcode': fake.postcode(),
        'patient_state': chosen_state,
        'referral_status': referral_status,
        'referral_accepted_rejected_date': referral_accepted_rejected_date
    }



def connect_to_database():
    """Establishes a connection to the PostgreSQL database and returns the connection object."""
    return psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        sslmode="require"
    )

def insert_ereferral_record(record):
    """Inserts a single eReferral record into the database and prints the SQL command."""
    # Base SQL statement for inserting data with placeholders for parameters
    insert_sql = """
    INSERT INTO ereferral (
        e_referral_id, referral_datetime, clinician_name, clinician_contact_details,
        healthcare_provider_number, practice_name, practice_contact_details,
        secure_messaging_provider, secure_messaging_endpoint, patient_first_name,
        patient_last_name, patient_contact_details, patient_alternate_contact_name,
        patient_alternate_contact_details, target_organisation_name, target_faculty,
        referral_reason, medication_history, comorbidity, patient_dob,
        medicare_number, medicare_expiry, atsi_code, primary_language_code, additional_info,
        patient_full_address, patient_email, patient_postcode, patient_state, referral_status, referral_accepted_rejected_date
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        record['e_referral_id'], record['referral_datetime'], record['clinician_name'], record['clinician_contact_details'],
        record['healthcare_provider_number'], record['practice_name'], record['practice_contact_details'],
        record['secure_messaging_provider'], record['secure_messaging_endpoint'], record['patient_first_name'],
        record['patient_last_name'], record['patient_contact_details'], record['patient_alternate_contact_name'],
        record['patient_alternate_contact_details'], record['target_organisation_name'], record['target_faculty'],
        record['referral_reason'], record['medication_history'], record['comorbidity'], record['patient_dob'],
        record['medicare_number'], record['medicare_expiry'], record['atsi_code'], record['primary_language_code'], record['additional_info'],
        record['patient_full_address'], record['patient_email'], record['patient_postcode'], record['patient_state'],
        record['referral_status'], record['referral_accepted_rejected_date']
    )

    connection = None
    try:
        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()
        # Print the SQL command for manual inspection or use
        # print(f"Executed SQL:\n{cursor.mogrify(insert_sql, values).decode('utf-8')}")
        
        # Execute the insertion
        cursor.execute(insert_sql, values)
        
        # Commit the transaction
        connection.commit()
        print("Record inserted successfully.")
        

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Clean up the database connection by closing it
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


# Example of generating a record and inserting it into the database
for _ in range(5000):
    ereferral_record = generate_ereferral_data()
    insert_ereferral_record(ereferral_record)
