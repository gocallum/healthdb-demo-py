import json


def extract_email(telecom_list):
    for telecom in telecom_list:
        if telecom['system'] == 'email':
            return telecom['value']
    return None  # Returns None if no email is found


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
                'gender': item['gender'],
                # get patient id 
                'id': item['id'],
                # get patient address line 1
                'address_line_1': item['address'][0]['line'][0],
                # get patient city 
                'city': item['address'][0]['city'],
                # get patient postcode
                'postcode': item['address'][0]['postalCode'],
                # get patient state 
                'state': item['address'][0]['state'],
                # get patient date of birth
                'dob': item['birthDate'],
                # get patient phone number
                'phone_mobile': item['telecom'][0]['value'],
                'phone_home': item['telecom'][1]['value'],
                'email': extract_email(item.get('telecom', [])),
                'dva_number': next((identifier['value'] for identifier in item['identifier'] if identifier.get('type', {}).get('coding', [{}])[0].get('code') == 'DVAU'), None),
                # get the patient's medicare expiry date
                #'medicare_expiry': item['extension'][0]['valueDate'],
                #get the patient's carer information 
                'carer_name': item['contact'][0]['name']['family'] + ' ' + ' '.join(item['contact'][0]['name']['given']),
                'carer_phone': item['contact'][0]['telecom'][0]['value'],
                'carer_email': extract_email(item['contact'][0]['telecom']),
                'carer_relationship': item['contact'][0]['relationship'][0]['coding'][0]['display'],
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
