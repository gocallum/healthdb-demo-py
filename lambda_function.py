# lambda_function.py
import json
from parse_ereferrals_fhir import extract_entities

def lambda_handler(event, context):
    try:
        fhir_payload = json.loads(event['body'])
        entities = extract_entities(fhir_payload)
        
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

    try:
        # Load the sample data from a file
        with open(r'data\sample1.json', 'r') as file:
            data = json.load(file)
            # Example FHIR payload as you might receive from an API trigger
        example_event = {
            'body': json.dumps(
                data
            )
        }
        
        # Simulate an empty context
        example_context = {}
        
        # Call lambda_handler with the example event and context
        response = lambda_handler(example_event, example_context)
        print(response)
    except FileNotFoundError:
        print("File not found. Please check the file path.")
    else:
        print("error loading file.") 
        exit(1)



