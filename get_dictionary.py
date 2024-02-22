import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed

def fetch_and_save_content(stem, base_url, root_directory):
    """
    Fetches content for a given stem and saves it to the corresponding HTML file.
    Handles rate limiting by pausing and sending test requests until the limit is lifted.
    """
    # Construct the URL for the current stem
    url = base_url + stem
    while True:  # Keep trying until successful
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                left_content = soup.find('div', class_='left-content')
                content_str = str(left_content) if left_content else 'Content not found'
                subdirectory_path = os.path.join(root_directory, stem[0], stem[:2])
                os.makedirs(subdirectory_path, exist_ok=True)
                file_path = os.path.join(subdirectory_path, f'{stem}.html')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content_str)
                return f"Saved: {stem}"
            elif response.status_code == 429 or response.status_code == 403:  # Rate limit detected
                print(f"Rate limit reached, pausing requests. Retrying {stem} in 60 seconds...")
                sleep(60)  # Wait for 60 seconds before retrying
            else:
                return f"Failed ({response.status_code}): {stem}"
        except Exception as e:
            return f"Error: {stem} - {e}"

def main(stems, base_url, root_directory):
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(fetch_and_save_content, stem, base_url, root_directory) for stem in stems]
        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    # Start time
    start_time = datetime.now()

    # Load the stems
    source_directory = 'word_lists'
    # source_file_path = os.path.join(source_directory, 'word_stems.json')
    source_file_path = os.path.join(source_directory, 'exclusive_to_json.json')
    with open(source_file_path, 'r') as file:
        # 30 --> abashless (line 32)

        # Previous Runs:
        # stems = json.load(file)[:10]
        # stems = json.load(file)[10:20]
        # stems = json.load(file)[30:1000]
        # stems = json.load(file)[1000:1100]
        # stems = json.load(file)[1100:2000]
        # stems = json.load(file)[2000:3000]
        # stems = json.load(file)[3000:4000]
        # stems = json.load(file)[4000:121860] (Rate Limited)
        # stems = json.load(file)[7520:121860] (Rate Limited)
        # stems = json.load(file)[18100:121860] (Success)

        # Current Run
        stems = json.load(file)

    # Definitions
    base_url = "https://www.merriam-webster.com/dictionary/"
    root_directory = 'raw_dictionary'
    os.makedirs(root_directory, exist_ok=True)

    # Process the stems
    main(stems, base_url, root_directory)

    # End time and duration
    end_time = datetime.now()
    print(f"Script started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Script ended at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {end_time - start_time}")
