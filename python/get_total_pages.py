import requests
from bs4 import BeautifulSoup
import json

# Base URL pattern
base_url = "https://www.merriam-webster.com/browse/dictionary/{}/1"

# Initialize an empty dictionary to store the total pages for each letter
total_pages_dict = {}

# Iterate through each letter of the alphabet
for letter in 'abcdefghijklmnopqrstuvwxyz':
    # Construct the URL
    url = base_url.format(letter)
    
    # Send a GET request to fetch the page content
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the first span element with the class "counters"
        span = soup.find('span', class_='counters')
        
        # Extract the total number of pages from the span's text
        total_pages = span.text.split(' ')[-1] if span else 'Unknown'
        
        # Update the dictionary with the letter as the key and total pages as the value
        total_pages_dict[letter] = total_pages
    else:
        print(f"Failed to fetch data for letter '{letter}'.")

# Save the dictionary to a separate file (e.g., total_pages.json)
with open('total_pages.json', 'w') as file:
    json.dump(total_pages_dict, file, indent=4)

print("The total pages dictionary has been saved to total_pages.json.")