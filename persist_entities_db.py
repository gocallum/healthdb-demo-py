import json
import os
from parse_ereferrals_fhir import extract_entities
from dotenv import load_dotenv
import psycopg2


# Load environment variables from .env file
load_dotenv()

# Database credentials from the .env file
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_DB = os.getenv("POSTGRES_DATABASE")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")


def load_json_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return None
    except json.JSONDecodeError:
        print("Failed to decode JSON. Please check the file content.")
        return None

def db_save_entities(entities):
    # Implement the database save operation here
    # Use the POSTGRES_* environment variables to connect to the database
    # Save the entities to the database
    
    conn = None
    try:
        conn = psycopg2.connect(
            dbname=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST
        )
        cur = conn.cursor()

        sql = """
        INSERT INTO inbound_referral (
            patient_first_name, patient_last_name, patient_medicare_number, patient_gender,
            patient_address_line_1, patient_city, patient_postcode, patient_state, patient_dob,
            patient_phone_mobile, patient_phone_home, patient_email, patient_dva_number,
            patient_carer_name, patient_carer_phone, patient_carer_email, patient_carer_relationship,
            practitioner_first_name, practitioner_last_name, practitioner_npi,
            practice_name, practice_identifier, practice_address, practice_email,
            practice_phone, practice_edi_system, practice_edi_id,
            referrer_id, referrer_medicare_provider_number, referrer_organization_reference,
            referrer_practitioner_reference
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        # Assuming 'entities' is a dict containing all the data extracted and structured
        cur.execute(sql, (
            entities['patient']['first_name'], entities['patient']['last_name'], entities['patient']['medicare_number'], entities['patient']['gender'],
            entities['patient']['address_line_1'], entities['patient']['city'], entities['patient']['postcode'], entities['patient']['state'], entities['patient']['dob'],
            entities['patient']['phone_mobile'], entities['patient']['phone_home'], entities['patient']['email'], entities['patient']['dva_number'],
            entities['patient']['carer_name'], entities['patient']['carer_phone'], entities['patient']['carer_email'], entities['patient']['carer_relationship'],
            entities['practitioner']['first_name'], entities['practitioner']['last_name'], entities['practitioner']['npi'],
            entities['practice']['name'], entities['practice']['identifier'], entities['practice']['address'], entities['practice']['email'],
            entities['practice']['phone'], entities['practice']['edi_system'], entities['practice']['edi_id'],
            entities['referrer']['id'], entities['referrer']['medicare_provider_number'], entities['referrer']['organization_reference'],
            entities['referrer']['practitioner_reference']
        ))


        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None and conn.closed == 0:
            conn.close()





def main():
    data = load_json_file(r'data\sample1.json')
    if data is None:
        return

    entities = extract_entities(data)
    db_save_entities(entities)
    print("Entities saved to the database.")



if __name__ == "__main__":
    main()
