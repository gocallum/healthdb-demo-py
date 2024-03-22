import json
import csv


def extract_patient_info(data):
    # Initialize variables to hold the extracted information
    patient_info = {}
    
    # Extract information from the payload
    for item in data['contained']:
        if item['resourceType'] == 'Patient':
            patient_info['Patient ID'] = item['id']
            aboriginal_status = next((ext for ext in item['extension'] if ext['url'].endswith('indigenous-status')), None)
            if aboriginal_status:
                patient_info['Aboriginal Status Code'] = aboriginal_status['valueCoding']['code']
                patient_info['Aboriginal Status Description'] = aboriginal_status['valueCoding']['display']
            # Assuming the first identifier is Medicare Number for simplicity
            patient_info['Medicare Number'] = item['identifier'][0]['value']
            # Extract name information
            name_info = item['name'][0]
            patient_info['Given Name'] = " ".join(name_info['given'])
            patient_info['Family Name'] = name_info['family']
            # Assuming the first telecom info contains desired contact information
            patient_info['Contact Information'] = {telecom['system']: telecom['value'] for telecom in item['telecom']}
            patient_info['Gender'] = item['gender']
            patient_info['Birth Date'] = item['birthDate']
            # Assuming the first address is the current address
            address_info = item['address'][0]
            patient_info['Address Line'] = " ".join(address_info['line'])
            patient_info['City'] = address_info['city']
            patient_info['State'] = address_info['state']
            patient_info['Postal Code'] = address_info['postalCode']
            patient_info['Country'] = address_info['country']
            break
    
    return patient_info


# Assuming `data` is the payload from the earlier provided `generate_referral()` function
# If reading from a file, use the commented lines below instead to load your JSON data
file_path = 'data\sample1.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Extract patient info from the referral data
patient_info = extract_patient_info(data)

# Writing to CSV
csv_file_path = 'output.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=patient_info.keys())
    writer.writeheader()
    writer.writerow(patient_info)

print("Data has been written to CSV file successfully.")
