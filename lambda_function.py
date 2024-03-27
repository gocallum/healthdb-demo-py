# lambda_function.py
import json
from parse_ereferrals_fhir import extract_entities
from persist_entities_db import db_save_entities

def lambda_handler(event, context):
    try:
        fhir_payload = json.loads(event['body'])
        entities = extract_entities(fhir_payload)
        db_save_entities(entities)
        print("Entities saved to the database.")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(entities)
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
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



