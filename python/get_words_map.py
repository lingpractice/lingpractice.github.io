import requests
from bs4 import BeautifulSoup
import json
import os

# Ensure the words_map directory exists
output_directory = 'words_map'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Load the total pages dictionary from the file
with open('total_pages.json', 'r') as file:
    total_pages_dict = json.load(file)

# Function to fetch and parse words from a single page
def fetch_words_from_page(letter, page):
    url = f"https://www.merriam-webster.com/browse/dictionary/{letter}/{page}"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        word_elements = soup.select('.mw-grid-table-list li a')
        words_map = {}
        for element in word_elements:
            stem = element['href'].split('/')[-1]
            inflection = element.find('span').text
            if stem in words_map:
                words_map[stem].append(inflection)
            else:
                words_map[stem] = [inflection]
        return words_map
    else:
        print(f"Failed to fetch or parse page {page} for letter '{letter}'")
        return {}

# Main function to process each letter
def process_letter(letter):
    words_map = {}
    total_pages = int(total_pages_dict.get(letter, 0))
    for page in range(1, total_pages + 1):
        words_page_map = fetch_words_from_page(letter, page)
        for stem, inflection in words_page_map.items():
            if stem in words_map:
                words_map[stem].extend(inflection)
            else:
                words_map[stem] = inflection
        print(f"Letter {letter}', Page '{page}' has been read.")
    return words_map

# Process each letter of the alphabet
for letter in 'defghijklmnopqrstuvwxyz':
    print(f"Processing letter '{letter}'...")
    words_map_for_letter = process_letter(letter)

    # Save the words map to a file within the words_map directory
    output_filename = os.path.join(output_directory, f'words_map_{letter}.json')
    with open(output_filename, 'w') as file:
        json.dump(words_map_for_letter, file, indent=4)

    print(f"The words map for letter '{letter}' has been saved to {output_filename}.")
