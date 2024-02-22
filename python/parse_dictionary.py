# #left-content - Content Container


# #dictionary-entry-1 - Each state of the word (i.e. noun, verb, adjective)

    # [parent] .entry-header-content .hword - Entry Title
    # [parent] .entry-header-content .parts-of-speech a - Part of Speech

    # [parent] .word-syllables-prons-header-content a - Pronounciation (Only appears in first entry)

    # [parent] .vg - Outer definition category container (1, 2, 3...)
        # [parent] #vd - Verb Type
        # [parent] .vg-sseq-entry-item - Defintion category container (a, b, c...)

            # [parent] .sb-entry - Inner defintion category container (a1, a2, a3...)
                # [parent] .sense-content - Defintion Container
                    # [parent] .badge - Badge text
                        # [parent] .dt - Definition Text Container
                            # [parent] .dtText [text] - Default Text (Req.)
                            # [parent] .dtText strong - Strong text, usually for colons
                            # [parent] .dtText a - Links

                            # [parent] .sub-content-thread - Subcontent when definition contains links
                                # [parent] .sents [text] - Defalt Text
                                # [parent] .sents em - Italicized Text
                                # [parent] .sents pe-2 - Em-Dash
                            # [parent] .sub-content-thread
                            # [parent] .sub-content-thread
                            # [parent] etc...

                            # [parent] .uns - Arrow (Can contain .sub-content-thread --> see run)

                    # [parent] .sdsense - Defintion Information Container
                        # [parent] .sd - Information Header
                        # [parent] .dtText - Information Text
                # [parent] .sense-content
                # [parent] .sense-content
                # [parent] etc...
            # [parent] .sb-entry
            # [parent] .sb-entry
            # etc...

    # #dictionary-entry-1 .vg-sseq-entry-item
    # #dictionary-entry-1 .vg-sseq-entry-item
    # etc...

    # Abbriviations:

# #dictionary-entry-2
# #dictionary-entry-3
# etc...

# #phrases - phrases containing the word (run a fever) (Situational)

# #anchor-seporator - Separates defintions and other information about the word

# #synonyms - Word synonyms

# #examples - Example usage in a sentence

# After: #word history, #related-phrases, #related-articles, #nearby-entries
# After: #citations, #social-links, .widget .more_defs, #more-from-mw

import os
from bs4 import BeautifulSoup
from datetime import datetime

def parseFile(source_file_path):
    
    # Read the content of the source file
    with open(source_file_path, 'r') as file:
        html_content = file.read()
    
    # Step 2: Parse the HTML content with BeautifulSoup
    html = BeautifulSoup(html_content, 'html.parser')

    # Step 3: Do something with the parsed HTML
    # div = html.find('div', id='dictionary-entry-1')

    dictionary_entries = html.find_all('div', class_='entry-word-section-container')
    isInterjection = False
    for entry in dictionary_entries:
        pos_tag = entry.select_one('.entry-header-content .parts-of-speech a')
        if pos_tag and pos_tag.text.strip().lower() == 'interjection':
            isInterjection = True
            break
    
    return isInterjection

    # To get the HTML of the div as a string
    # div_html = str(div)
    # To extract text from the div
    # div_text = div.get_text()

    # print(dictionary_entries)

import os
import json

def find_files(directory):
    iterable = 0
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.html'):
                filePath = os.path.join(subdir, filename)
                output = parseFile(filePath)
                if (output):
                    interjections_set.add(filename[:-5])
                iterable += 1
    print(iterable)
    return 


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

interjections_set = set()

def main():
    # raw_dictionary_path = 'raw_dictionary'
    raw_dictionary_dir = 'raw_dictionary'
    raw_dictionary_path = 'raw_dictionary/p/pi/pish.html'
    # raw_dictionary_path = 'raw_dictionary/a/al/alas.html'
    word_stems_path = 'word_lists/interjections.json'
    word_lists_dir = 'word_lists'

    words_limit = False  # Adjust this number as needed

    outcome = parseFile(raw_dictionary_path)
    print(outcome)

    html_files = find_files(raw_dictionary_dir)
    # word_stems = read_word_stems(word_stems_path, limit=words_limit)

    # compare_and_save_lists(html_files, word_stems, word_lists_dir)

    sorted_interjections_list = sorted(list(interjections_set))
    js_file_path1 = os.path.join(word_lists_dir, 'interjections.js')
    with open(js_file_path1, 'w') as js_file:
        js_file.write('const INTERJECTION_LIST = [\n')
        js_file.write(',\n'.join(f'  "{interjection}"' for interjection in sorted_interjections_list))
        js_file.write('\n];\n')

if __name__ == "__main__":
    main()