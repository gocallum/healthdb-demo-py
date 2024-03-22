import json

# Assuming `data` is your JSON structure loaded from the sample provided or a similar source
# If you need to load from a file: 

with open('data\sample1.json', 'r') as file:
     data = json.load(file)

def extract_entities(data):
    patient = {}
    practitioner = {}
    practice = {}
    referrer = {}

    for item in data['contained']:
        if item['resourceType'] == 'Patient':
            patient = {
                'first_name': ' '.join(item['name'][0]['given']),
                'last_name': item['name'][0]['family'],
                'medicare_number': next((identifier['value'] for identifier in item['identifier'] if identifier.get('type', {}).get('coding', [{}])[0].get('code') == 'MC'), None),
                'gender': item['gender']
            }
        elif item['resourceType'] == 'Practitioner':
            practitioner = {
                'first_name': ' '.join(item['name'][0]['given']),
                'last_name': item['name'][0]['family'],
                'npi': next((identifier['value'] for identifier in item['identifier'] if identifier.get('type', {}).get('coding', [{}])[0].get('code') == 'NPI'), None)
            }
        elif item['resourceType'] == 'Organization':
            practice = {
                'name': item['name'],
                'identifier': next((identifier['value'] for identifier in item['identifier'] if identifier.get('type', {}).get('coding', [{}])[0].get('code') == 'NOI'), None),
                'address': ', '.join(item['address'][0]['line']) + ', ' + item['address'][0]['city'] + ', ' + item['address'][0]['state'] + ' ' + item['address'][0]['postalCode'] + ', ' + item['address'][0]['country']
            }
        # Assuming Referrer is a PractitionerRole, adjust as needed
        elif item['resourceType'] == 'PractitionerRole':
            referrer = {
                'id': item['id'],
                'medicare_provider_number': next((identifier['value'] for identifier in item['identifier'] if identifier.get('type', {}).get('coding', [{}])[0].get('code') == 'UPIN'), None),
                'organization_reference': item['organization']['reference'],
                'practitioner_reference': item['practitioner']['reference']
            }

    return {
        'patient': patient,
        'practitioner': practitioner,
        'practice': practice,
        'referrer': referrer
    }

# Extract entities
entities = extract_entities(data)

# Example of printing the structured data
print("Patient:", entities['patient'])
print("Practitioner:", entities['practitioner'])
print("Practice:", entities['practice'])
print("Referrer:", entities['referrer'])
