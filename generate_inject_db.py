from faker import Faker
import random
from psycopg2 import extras  # This is the missing import
import psycopg2
import os

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

def generate_healthcare_concern():
    # Predefined list of healthcare concern templates
    healthcare_concerns = [
        "Patient has a broken shoulder.",
        "Complaints of chronic back pain.",
        "Suspected case of viral infection.",
        "Experiencing severe migraines.",
        "Requires evaluation for possible diabetes.",
        "Symptoms suggest acute bronchitis.",
        "High blood pressure needing management.",
        "Potential allergic reaction identified.",
        "Injury from a recent fall.",
        "Consultation for anxiety and depression.",
        "Routine check-up for heart disease risk.",
        "Follow-up on previous surgical procedure.",
        "Early signs of osteoporosis observed.",
        "Assessment for autoimmune diseases.",
        "Examination for skin rash and eczema.",
        "Concerns regarding childhood vaccinations.",
        "Dental pain and possible cavity.",
        "Screening for breast cancer.",
        "Evaluating nutritional deficiencies.",
        "Symptoms of sleep disorders.",
        "Review of medication side effects.",
        "Consultation requested for weight management.",
        "Testing for thyroid function abnormalities.",
        "Consideration for vision and eye health.",
        "Hearing loss and tinnitus evaluation.",
        "Chronic fatigue and possible fibromyalgia.",
        "Pregnancy check-up and prenatal care.",
        "Suspected gastrointestinal issues.",
        "Investigation into frequent headaches.",
        "Concerns about aging and memory loss.",
        "Fitness assessment for sports participation.",
        "Risk assessment for genetic conditions.",
        "Evaluation for chronic kidney disease.",
        "Symptoms of urinary tract infection.",
        "Monitoring for liver function abnormalities.",
        "Assessment for reproductive health issues.",
        "Concerns about vitamin D deficiency.",
        "Possible concussion from recent head injury.",
        "Screening for prostate cancer.",
        "Consultation for sleep apnea.",
        "Evaluation of joint pain for arthritis.",
        "Treatment options for acid reflux and GERD.",
        "Investigation of unexplained weight loss.",
        "Check-up for asthma control and management.",
        "Preventive vaccination for seasonal flu.",
        "Assessment for attention deficit hyperactivity disorder.",
        "Counseling for stress management and burnout.",
        "Diagnostic testing for Lyme disease.",
        "Management of menopause symptoms.",
        "Follow-up on abnormal blood test results.",
        "Therapy options for chronic sinusitis.",
        "Pre-operative evaluation for elective surgery.",
        "",  # Represents a potential for no specific concern listed
    ]

    # Randomly select from the predefined list
    return random.choice(healthcare_concerns)



def generate_australian_gp_name(state):
    # Predefined GP practice names to simulate real names. You can add more or adjust as needed.
    predefined_names = [
        "Harbour City Medical Centre",
        "Springfield General Practice",
        "Green Valley Family Clinic",
        "Oceanview Medical Practice",
        "Mountain Ridge Health Centre",
        "Riverbank Family Health",
        "Sunnybank Community Clinic",
        "Bayview Medical Associates",
        "Outback Health Services",
        "Coastline Primary Care",
        "Blue Mountains Medical Group",
        "Gold Coast Health Partners",
        "Urban Wellness Clinic",
        "Coral Sea Healthcare",
        "Desert Springs Medical Practice",
        "Rainforest Medical Network",
        "Sunshine State Health Centre",
        "Great Barrier Reef Medical Clinic",
        "Red Centre Family Practice",
        "Tropical North Health Services",
        "Southern Cross Medical Care",
        "East Coast Family Medicine",
        "West End Medical Practice",
        "Northern Rivers Healthcare",
        "Surfside Community Health"
    ]
    # Append a state abbreviation to make it more specific
    return random.choice(predefined_names) + f" ({state})"

def get_target_organisation_name():
    specialist_clinics = [
        "Sydney Cardiology Group",
        "Melbourne Neurology Centre",
        "Brisbane Orthopedics Clinic",
        "Perth Paediatrics Practice",
        "Adelaide Oncology Associates",
        "Canberra Radiology Network",
        "Gold Coast Emergency Specialists",
        "Hobart Endocrinology & Diabetes Service",
        "Darwin Gastroenterology Group",
        "Sunshine Coast Rheumatology Clinic",
        "Geelong Pulmonary and Sleep Medicine",
        "Cairns Allergy Clinic",
        "Alice Springs Pain Management Center",
        "Townsville Dermatology Clinic",
        "Launceston Urology Practice",
        "Bendigo Women's Health Institute",
        "Toowoomba Cardiac Centre",
        "Mackay Mental Health Services",
        "Rockhampton Eye Clinic",
        "Wollongong ENT Specialists"
    ]
    return random.choice(specialist_clinics)


def generate_ereferral_data():
    # Randomly choose an Australian state for consistency in GP name and patient address
    states = ['NSW', 'VIC', 'QLD']
    chosen_state = random.choice(states)
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
        'referral_datetime': fake.date_time_this_decade(before_now=True, after_now=False, tzinfo=None),
        'clinician_name': fake.name(),
        'clinician_contact_details': fake.phone_number(),
        'healthcare_provider_number': fake.bothify(text='????#####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        'practice_name': generate_australian_gp_name(chosen_state),
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
        'comorbidity': fake.text(max_nb_chars=100),
        'patient_dob': fake.date_of_birth(minimum_age=5, maximum_age=115),
        'medicare_number': fake.bothify(text='#### #### ##'),  # Adjusted to fit the Medicare format
        'medicare_expiry': fake.date_this_decade(before_today=True, after_today=False),
        'atsi_code': random.randint(1, 3),
        'primary_language_code': random.randint(1, 100),
        'additional_info': fake.text(max_nb_chars=200),
        'patient_full_address': fake.address(),
        'patient_email': fake.email(),
        'patient_postcode': fake.postcode(),
        'patient_state': chosen_state
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
        patient_full_address, patient_email, patient_postcode, patient_state
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    values = (
        record['e_referral_id'], record['referral_datetime'], record['clinician_name'], record['clinician_contact_details'],
        record['healthcare_provider_number'], record['practice_name'], record['practice_contact_details'],
        record['secure_messaging_provider'], record['secure_messaging_endpoint'], record['patient_first_name'],
        record['patient_last_name'], record['patient_contact_details'], record['patient_alternate_contact_name'],
        record['patient_alternate_contact_details'], record['target_organisation_name'], record['target_faculty'],
        record['referral_reason'], record['medication_history'], record['comorbidity'], record['patient_dob'],
        record['medicare_number'], record['medicare_expiry'], record['atsi_code'], record['primary_language_code'], record['additional_info'],
        record['patient_full_address'], record['patient_email'], record['patient_postcode'], record['patient_state']
    )

    connection = None
    try:
        # Connect to the database
        connection = connect_to_database()
        cursor = connection.cursor()
        # Print the SQL command for manual inspection or use
        print(f"Executed SQL:\n{cursor.mogrify(insert_sql, values).decode('utf-8')}")
        
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
for _ in range(100):
    ereferral_record = generate_ereferral_data()
    insert_ereferral_record(ereferral_record)
