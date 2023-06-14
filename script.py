import vobject
import requests
import time
import re

# Define constants
url = "https://api.maytapi.com/api/a2702d97-f557-45a3-8962-ad51c6e86d65/29620/group/add"
headers = {
    "accept": "application/json",
    "x-maytapi-key": "bd4e48da-6463-4620-b094-2a63571f6ffd",
    "Content-Type": "application/json"
}
added_numbers_file = 'added_numbers.txt'

# Open and read the vcf file
with open('contacts.vcf', 'r') as f:
    vcf_text = f.read()

# Extract phone numbers from the vcf file
phone_numbers = []
for vcard in vobject.readComponents(vcf_text):
    if hasattr(vcard, 'tel'):  # Check if vcard has 'tel' attribute
        number = re.sub('[^0-9]', '', vcard.tel.value)  # Extract only digits
        if number:
            phone_numbers.append(number)
            if len(phone_numbers) >= 100:  # Limit to the first 100 contacts
                break

# Load the added numbers
try:
    with open(added_numbers_file, 'r') as f:
        added_numbers = f.read().splitlines()
except FileNotFoundError:
    # If the file doesn't exist yet, create it with these numbers already added
    added_numbers = ['601170250221', '34625818630', '34625818617']
    with open(added_numbers_file, 'w') as f:
        for number in added_numbers:
            f.write(number + '\n')

# Send POST requests at 6-minute intervals
for number in phone_numbers:
    if number in added_numbers:
        print(f"Skipping {number}, already added.")
        continue

    data = {
        "conversation_id": "120363160537707852@g.us",
        "number": f"{number}@c.us"
    }

    try:
        print(f"Adding {number}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises a HTTPError if the response status is 4xx, 5xx
        print(response.json())

        # Add the number to the added_numbers list and write it to the file
        added_numbers.append(number)
        with open(added_numbers_file, 'a') as f:
            f.write(number + '\n')

    except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as err:
        print(f"An error occurred: {err}")
        continue

    time.sleep(360)  # Wait for 6 minutes
