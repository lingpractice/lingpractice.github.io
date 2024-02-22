import os
import json

# Define the source directory
source_directory = 'filtered_words_map'
target_directory = 'word_lists'

# Create the target directory if it doesn't exist
if not os.path.exists(target_directory):
    os.makedirs(target_directory)

# Initialize sets to hold unique inflections and stems
inflections_set = set()
stems_set = set()
stem_map = {}

# Iterate through each file in the source directory
for filename in os.listdir(source_directory):
    if filename.endswith('.json'):
        source_file_path = os.path.join(source_directory, filename)
        # Read the content of the source file
        with open(source_file_path, 'r') as file:
            words_map = json.load(file)
            # Add inflections and stems to the respective sets
            for stem, inflections in words_map.items():
                stems_set.add(stem)
                inflections_set.update(inflections)
                for inflections in inflections:
                    stem_map[inflections] = stem

# Convert sets to sorted lists
sorted_inflections_list = sorted(list(inflections_set))
sorted_stems_list = sorted(list(stems_set))

# Write the inflections to a JavaScript file
js_file_path1 = os.path.join(target_directory, 'word_list.js')
with open(js_file_path1, 'w') as js_file:
    js_file.write('const WORD_LIST = [\n')
    js_file.write(',\n'.join(f'  "{inflection}"' for inflection in sorted_inflections_list))
    js_file.write('\n];\n')

print(f"JavaScript file {js_file_path1} has been created with all inflections.")

# Write the stems to a JSON file

json_file_path = os.path.join(target_directory, 'word_stems.json')
with open(json_file_path, 'w') as json_file:
    json.dump(sorted_stems_list, json_file, indent=4)

print(f"JSON file {json_file_path} has been created with all stems.")

# Write the stem_map to a JavaScript file
js_file_path2 = os.path.join(target_directory, 'stem_map.js')
with open(js_file_path2, 'w') as js_file:
    js_file.write('const STEM_MAP = ')
    json.dump(stem_map, js_file, indent=4)
    js_file.write(';\n')

print(f"JavaScript file {js_file_path2} has been created with root-to-stem mappings.")
