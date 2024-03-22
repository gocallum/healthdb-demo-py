import json


def extract_email(telecom_list):
    for telecom in telecom_list:
        if telecom['system'] == 'email':
            return telecom['value']
    return None  # Returns None if no email is found



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
                'address': ', '.join(item['address'][0]['line']) + ', ' + item['address'][0]['city'] + ', ' + item['address'][0]['state'] + ' ' + item['address'][0]['postalCode'] + ', ' + item['address'][0]['country'],
                # get the practice's phone number
                'email': extract_email(item.get('telecom', [])),
                'phone': item['telecom'][0]['value'],  
                'edi_system': next((identifier['system'] for identifier in item['identifier'] if identifier.get('type', {}).get('coding', [{}])[0].get('code') == 'RI'), None),
                'edi_id' : next((identifier['value'] for identifier in item['identifier'] if identifier.get('type', {}).get('coding', [{}])[0].get('code') == 'RI'), None),
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


def main():
    try:
        with open(r'data\sample1.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print("File not found. Please check the file path.")
        return
    except json.JSONDecodeError:
        print("Failed to decode JSON. Please check the file content.")
        return

    entities = extract_entities(data)

    # Example of printing the structured data
    print("Patient:", entities.get('patient'))
    print("Practitioner:", entities.get('practitioner'))
    print("Practice:", entities.get('practice'))
    print("Referrer:", entities.get('referrer'))

if __name__ == "__main__":
    main()
