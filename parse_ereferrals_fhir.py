import json


def parse_payload(file_path):
    with open(file_path, 'r') as file:
        # Load and parse the JSON payload
        payload = json.load(file)

    # Extract and store key attributes for each object
    parsed_data = {
        'practitioner': [],
        'organizations': [],
        'patient': [],
        'referral': []
    }

    # Assuming the structure includes these elements directly or within "contained"
    if 'contained' in payload:
        for item in payload['contained']:
            if item['resourceType'] == 'Practitioner':
                parsed_data['practitioner'].append({'id': item['id'], 'name': item.get('name', [])})
            elif item['resourceType'] == 'Organization':
                parsed_data['organizations'].append({'id': item['id'], 'name': item.get('name', '')})
            elif item['resourceType'] == 'Patient':
                parsed_data['patient'].append({'id': item['id'], 'name': item.get('name', [])})
    
    # Directly accessing attributes of the referral itself
    parsed_data['referral'] = {
        'id': payload.get('id', ''),
        'status': payload.get('status', ''),
        'intent': payload.get('intent', ''),
        'priority': payload.get('priority', '')
    }

    return parsed_data

# Path to your generated payload JSON file
file_path = 'data\sample1.json'

# Parse the payload

parsed_data = parse_payload(file_path)

print (parsed_data['practitioner'])
print (parsed_data['organizations'])
print (parsed_data['patient'])
