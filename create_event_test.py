import json

# Path to the source file and the output file
source_file_path = 'data/sample1.json'
output_file_path = 'data/event1.json'

# Open and read the contents of the source JSON file
with open(source_file_path, 'r') as source_file:
    # Load the JSON data from the file
    data = json.load(source_file)
    
    # Create the test event structure by setting the body with the loaded JSON data
    test_event = {
        "body": json.dumps(data)  # Convert the JSON object to a string to simulate an API Gateway event
    }
    
    # Write the test event to the output file
    with open(output_file_path, 'w') as output_file:
        json.dump(test_event, output_file, indent=4)  # Write JSON data with indentation for readability

print(f'Test event has been written to {output_file_path}')
