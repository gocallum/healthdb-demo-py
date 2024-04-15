# lambda_function.py
import json
from fhir_response import send_error_response, send_success_response
from parse_ereferrals_fhir import extract_entities
from persist_entities_db import db_save_entities

def lambda_handler(event, context):
    try:
        fhir_payload = json.loads(event['body'])
        entities = extract_entities(fhir_payload)
        db_save_entities(entities)
        print("Entities saved to the database.")

        # compose the response
        diagnostics = 'Entities saved to the database.'
 
    
        return {
            'statusCode': 202,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': send_success_response(diagnostics)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': send_error_response(str(e))
        }

if __name__ == "__main__":
    file_path = 'data\\event1.json'
    try:
        # Load the sample data from a file
        # Example FHIR payload as you might receive from an API trigger

        with open(r'data\\event1.json', 'r') as file:
            test_event = json.load(file)


        # Simulate an empty context
        example_context = {}
        
        # Call lambda_handler with the example event and context
        response = lambda_handler(test_event, example_context)
        print(response)
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    except Exception as error:
        print(error) 
        exit(1)



