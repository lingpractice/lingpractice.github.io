import os
import json
import re

# Define the source and target directories
source_directory = 'words_map'
target_directory = 'filtered_words_map'

# Create the target directory if it doesn't exist
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

# Function to check if a string contains only lowercase alphabetic characters and is greater than 4 letters long
def is_valid(s):
    return re.fullmatch(r'[a-z]{4,}', s) is not None

# Iterate through each file in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.json'):
        # Construct the full path for the source file
        source_file_path = os.path.join(source_directory, filename)
        
        # Read the content of the source file
        with open(source_file_path, 'r') as file:
            words_map = json.load(file)
        
        # Filter the words map
        filtered_words_map = {
            key: [word for word in value if is_valid(word)]
            for key, value in words_map.items() if is_valid(key)
        }
        
        # Remove keys with empty lists after filtering
        filtered_words_map = {key: value for key, value in filtered_words_map.items() if value}
        
        # Construct the full path for the target file
        target_file_path = os.path.join(target_directory, filename)
        
        # Save the filtered words map to the target file
        with open(target_file_path, 'w') as file:
            json.dump(filtered_words_map, file, indent=4)

        print(f"Processed and saved filtered map for {filename}")
