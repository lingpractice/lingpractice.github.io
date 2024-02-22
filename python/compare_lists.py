import os
import json

def find_files(directory):
    """Recursively finds all files in the given directory and its subdirectories."""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith('.html'):
                files.append(filename[:-5])  # Remove .html extension
    return files

def read_word_stems(filepath, limit=None):
    """Reads words from a JSON file, optionally limiting the number of words returned."""
    with open(filepath, 'r') as file:
        words = json.load(file)
    return words[:limit] if limit else words

def save_list_to_json(data, filepath):
    """Saves a list of words to a JSON file."""
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)

def compare_and_save_lists(html_words, word_stems, directory):
    """Compares two lists of words and saves the exclusive lists into separate JSON files."""
    exclusive_to_html = [word for word in html_words if word not in word_stems]
    exclusive_to_json = [word for word in word_stems if word not in html_words]

    save_list_to_json(exclusive_to_json, os.path.join(directory, 'exclusive_to_json.json'))
    save_list_to_json(exclusive_to_html, os.path.join(directory, 'exclusive_to_html.json'))

def main():
    print("A")
    raw_dictionary_path = 'raw_dictionary'
    word_stems_path = 'word_lists/word_stems.json'
    word_lists_dir = 'word_lists'
    words_limit = False  # Adjust this number as needed

    html_files = find_files(raw_dictionary_path)
    word_stems = read_word_stems(word_stems_path, limit=words_limit)

    compare_and_save_lists(html_files, word_stems, word_lists_dir)
    print("DONE")

if __name__ == "__main__":
    main()
