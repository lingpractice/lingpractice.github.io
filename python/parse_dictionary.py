# #left-content - Content Container


# #dictionary-entry-1 - Each state of the word (i.e. noun, verb, adjective)

    # [parent] .entry-header-content .hword - Entry Title
    # [parent] .entry-header-content .parts-of-speech a - Part of Speech

    # [parent] .word-syllables-prons-header-content a - Pronounciation (Only appears in first entry)

    # [parent] .vg - Outer definition category container (1, 2, 3...)
        # [parent] #vd - Verb Divider
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

    # Abbreviations:

# #dictionary-entry-2
# #dictionary-entry-3
# etc...

# #phrases - phrases containing the word (run a fever) (Situational)

# #anchor-seporator - Separates defintions and other information about the word

# #synonyms - Word synonyms

# #examples - Example usage in a sentence

# After: #word history, #related-phrases, #related-articles, #nearby-entries
# After: #citations, #social-links, .widget .more_defs, #more-from-mw

# Example Homograph
example_homograph = {
    'meta': {
        'id': "run:2", # Word ID
        'offensive': False, # Initalize as False, set to True later if Offensive label
    },
    'hom': 3, # Homograph Number (Which entry are we in)
    'hwi': { # Headword Information
        'hw': "run", # Headword
    },
    'fl': 'noun',
    'lbs': [
        'often capitalized',
        'often attributive'
    ],
    'def': [
        {
            'vd': 'transitive verb',
            'sseq':[ # Sense Sequence
                [ # Arabic Sequence (1, 2, 3)
                    [ # Alphabetical Sequence (a, b, c)
                        'sense', # or 'bs' or 'pseq'
                        {
                            'sn': '1 a', # Sense Number
                            'sgram': 'T\/I', # Transitive, Intransitive
                            'sls': [
                                'chiefly British',
                                'sometimes offensive'
                            ],
                            'dt': [],
                            'sdsense':
                                {
                                },
                        }
                    ], [...]
                ], [...]
            ]
        }, ...
    ]
}

import os
from bs4 import BeautifulSoup
from datetime import datetime
import json

def custom_strip(string):
    # Check for whitespace at the beginning and end of the string
    start_space = string[:1].isspace()
    end_space = string[-1:].isspace()
    # Strip all whitespace characters from the beginning and end
    stripped_string = string.strip()
    # Re-add the space at the beginning and end if it was present
    if start_space:
        stripped_string = ' ' + stripped_string
    if end_space:
        stripped_string += ' '
    return stripped_string

def parseFile(dir, filename):
    
    filePath = os.path.join(dir, filename)
    with open(filePath, 'r') as file:
        html_content = file.read()
    
    html = BeautifulSoup(html_content, 'html.parser')
    word = filename[:-5] # Removes .html from filename
    json_list = [{
            'id': word,
            'offensive': False,
            'abridged': False,
            'parts_of_speech': []
    }]

    abridged = html.find('div', id='unabridged-promo')
    if abridged:
        json_list[0]["abridged"] = True
        json_output = json.dumps(json_list, indent=2)
        return json_output
    
    dictionary_entries = html.find_all('div', class_='entry-word-section-container')

    def iterate_dictionary_entries():
        for i, entry in enumerate(dictionary_entries, start=1):
            
            # Initiate Homograph
            homograph = {
                'meta': {
                    'id': word + ':' + str(i), # Word ID: ex. run:2 for second entry of run
                    'offensive': False, # Initalize as False, set to True later if Offensive label
                },
                'hom': i, # Homograph Number (Which entry are we in)
            }
            # Don't Use: psl vrs? vl? va?

            # Sense-Specific Grammatical Label (SGRAM)

            json_list.append(homograph)

            # Part of Speech / Functional Label (fl)
            part_of_speech_element = entry.find('h2', class_='parts-of-speech')
            if part_of_speech_element:
                part_of_speech = part_of_speech_element.text.split(' ')[0]
                homograph['fl'] = part_of_speech
                json_list[0]["parts_of_speech"].append(part_of_speech)

            # Pronounciation
            pronounciation_element = entry.find('span', class_='word-syllables-entry')
            if pronounciation_element:
                pronounciation = pronounciation_element.text
                homograph['hwi'] = {} # Headword Information
                homograph['hwi']['hw'] = pronounciation

            # Variants (vrs)
            variants_element = entry.find('span', class_='vrs')
            if variants_element:
                iterate_variants(variants_element, homograph)

            # General Label (lbs)
            general_label_element = entry.find('span', 'lbs')
            if general_label_element:
                homograph['lbs'] = general_label_element.text

            # Definition Section (def)
            definition_sections = entry.find_all('div', class_='vg')
            if definition_sections:
                homograph['def'] = []
                iterate_definition_section(definition_sections, homograph)

            # Cognate Cross-References (csx)
            cognate_cross_references = entry.find('p', class_='cxl-ref')
            if cognate_cross_references:
                homograph['csx'] = []
                tag_container(cognate_cross_references, homograph["csx"])

    def iterate_variants(variants_element, homograph):
        variant_array = []
        homograph['vrs'] = variant_array

        for variant in variants_element:
            if not variant.name:
                continue
            variant_class = variant.get('class', [])
            if 'badge' in variant_class:
                variant_array.append(['badge', variant.text])
            else:
                variant_label = list(variant.children)[0]
                variant_text = list(variant.children)[1]
                variant_array.append(['vl', variant_label.text])
                variant_array.append(['va', variant_text.text])


    def iterate_definition_section(definition_sections, homograph):
        for definition_section in definition_sections:
            # 'def': [
            #   {...} <-- Creates this object
            # ]
            definition = {}
            homograph['def'].append(definition)

            # 'def': [{...}, {
            # 'vd': 'transitive-verb' <-- Creates this key and value
            # }, {...}]
            verb_divider = definition_section.find('p', class_='vd')
            if verb_divider:
                definition['vd'] = verb_divider.text
            
            # 'def': [{...}, {
            # 'sseq': [] <-- Creates this key and value
            # }, {...}, {...}]
            sense_sequence_list = definition_section.find_all('div', class_='vg-sseq-entry-item')
            definition['sseq'] = []
            iterate_sense_sequence_list(sense_sequence_list, definition)

    def iterate_sense_sequence_list(sense_sequence_list, definition):
        for i, sense_sequence in enumerate(sense_sequence_list):
            # 'sseq': [
            #   [...] <-- Creates this list
            # ]
            sense_list = sense_sequence.find('div', class_='sb')
            definition['sseq'].append([])
            iterate_sense_list(sense_list, definition['sseq'][i])

    def iterate_sense_list(sense_list, sense_array):
        for sense in sense_list:
            if not sense.name:
                continue

            # 'sseq': [[...], [
            #   {...} <-- Creates this object
            # ], [...]]
            sense_dict = {}
            sense_array.append(sense_dict)

            # Sense Number
            sense_number = sense.find('span', class_='sn')
            if sense_number:
                sense_dict['sn'] = sense_number.text
            
            # Determine sense or truncated sense
            sense_element = sense.find('div', class_='sense')
            if sense_element:
                append_sense(sense_element, sense_dict)
                continue # Move to next element

            truncated_sense_element = sense.find('span', class_='sen')
            if truncated_sense_element:
                append_truncated_sense(truncated_sense_element, sense_dict)

    def append_sense(sense, sense_dict):
        # Sense Content
        sense_content = sense.find('div', class_='sense-content')

        for element in sense_content.children:
            if not element.name:
                continue

            element_class = element.get('class', [])
            # Badge (sls or spl)
            if 'spl' in element_class:
                sense_dict['sls'] = [element.text.strip()]
            elif 'badge' in element_class:
                set_badge(element, sense_dict)
            # Defining Text
            if 'et' in element_class:
                sense_dict["et"] = []
                tag_container(element, sense_dict["et"])
            if 'sgram' in element_class:
                sense_dict["sgram"] = []
                tag_container(element, sense_dict["sgram"])
            if 'dt' in element_class:
                set_defining_text(element, sense_dict)
            # Divided Sense
            if 'sdsense' in element_class:
                set_dividing_sense(element, sense_dict)
    
    def append_truncated_sense(sen, sense_dict):
        sen_element = sen.find('span', 'et')
        sense_dict["et"] = []
        if sen_element:
            tag_container(sen_element, sense_dict["et"])
        else:
            for element in list(sen)[2:]:
                # Ignore 1st element, which is sn element
                if not element.name:
                    continue
                sense_dict["et"].append(tag_element(element))

    def set_defining_text(defining_text, array):
        array['dt'] = []
        for element in defining_text.children:
            if not element.name:
                continue
            
            element_class = element.get('class', [])

            if 'dtText' in element_class:
                append_dt_text(element, array['dt'])
            elif 'uns' in element_class:
                append_usage_notes(element, array['dt'])
            elif 'sub-content-thread' in element_class: # vis element
                append_verbal_illustrations(element, array['dt'])
            elif 'snote' in element_class:
                append_supplemental_note(element, array['dt'])
            elif 'ca' in element_class:
                append_called_also(element, array['dt'])
    
    def set_dividing_sense(dividing_sense, array):
        array['sdsense'] = {}

        defining_text = []
        array['sdsense']['dt'] = defining_text

        for element in dividing_sense.children:

            if not element.name:
                # if element.text.strip(): # Add non-empty text
                #     array['sdsense'].append(['text', element.text.strip()])
                continue
            
            element_class = element.get('class', [])
            if 'sd' in element_class:
                array['sdsense']['sd'] = element.text
            if 'spl' in element_class:
                array['sdsense']['sls'] = [element.text.strip()]
            if 'badge' in element_class:
                array['sdsense']['sls'] = [element.text]
                set_badge(element, array['sdsense'])
            elif 'dtText' in element_class:
                append_dt_text(element, defining_text)
            elif 'uns' in element_class:
                append_usage_notes(element, defining_text)
            elif 'sub-content-thread' in element_class:
                append_verbal_illustrations(element, defining_text)
            elif 'snote' in element_class:
                append_supplemental_note(element, defining_text)
            elif 'ca' in element_class:
                append_called_also(element, defining_text)

    def set_badge(badge_element, array):
        array['sls'] = []
        for subject_label in badge_element.children:
            if not subject_label.name:
                if not subject_label.text.strip():
                    continue
            array['sls'].append(subject_label.text)
        
    
    def append_dt_text(defining_text_element, array):
        defining_text_container = ['dtText', []]
        array.append(defining_text_container)
        tag_container(defining_text_element, defining_text_container[1])
    
    def append_usage_notes(usage_notes_element, array):
        usage_notes_container = ['uns', []]
        array.append(usage_notes_container)

        for usage_note in usage_notes_element.children:
            if not usage_note.name:
                continue

            unage_note_array = []
            usage_notes_container[1].append(unage_note_array)
            tag_container(usage_note, unage_note_array)

    def append_verbal_illustrations(verbal_illustration_element, array):
        vis_container = ['vis', []]
        array.append(vis_container)
        
        # Loop, exclude last element, which is an empty text anchor
        for vis_element in verbal_illustration_element.children:
            if not vis_element.name:
                continue
            vis_element_class = vis_element.get('class', [])
            if 'thread-anchor' in vis_element_class:
                continue
            
            vis_element_tag, vis_tag_value = '', []
            if 'aq' in vis_element_class:
                # ToDo: Improve Attribution Quotes
                vis_element_tag = 'attribution_quote'
                vis_tag_value = ['text', vis_element.text]
            else:
                vis_element_tag = 'vis_text'
                tag_container(vis_element, vis_tag_value)

            vis_array = [vis_element_tag, vis_tag_value]
            vis_container[1].append(vis_array)

    def append_supplemental_note(supplemental_note_element, array):
        snote_container = ['snote', []]
        array.append(snote_container)

        for snote_element in supplemental_note_element.children:
            if not snote_element.name:
                if snote_element.text.strip(): # Add non-empty text
                    value = custom_strip(snote_element.text)
                    snote_container[1].append(['text', value])
                continue
            
            tagged_element = tag_element(snote_element)
            snote_container[1].append(tagged_element)
        
        # for snote_element in supplemental_note_element.children:
        #     if not snote_element.name:
        #         continue
            
        #     snote_element_class = snote_element.get('class', [])
        #     if 'note-txt' in snote_element_class:
        #         snote_container[1].append(['note-txt', ''])

    def append_called_also(called_also_element, array):
        ca_container = ['ca', {'cats': []}]
        array.append(ca_container)

        cats_array = ca_container[1]['cats']
        for ca_element in called_also_element.children:
            if not ca_element.name:
                continue

            ca_element_class = ca_element.get('class', [])
            if 'intro' in ca_element_class:
                ca_container[1]['intro'] = ca_element.text
            elif 'cat' in ca_element_class:
                cats_array.append(tag_element(ca_element))
            # Look into other tags that can be in ca elements

    def tag_container(container, array):
        # for element in container.children:
        for element in container:
            if not element.name and not element.text.strip():
                continue # Skip empty text
            tagged_element = tag_element(element)
            array.append(tagged_element)

    def tag_element(element):
        element_name = element.name
        tag = ''
        value = element.text
        if not element_name: # Default Text
            tag = 'text'
        else:
            # Troubleshoot by searching for empty tags ('') in the
            # JSON file, meaning that a category is missing here
            element_class = element.get('class', [])
            if 'mw_t_bc' in element_class: # Colon Space
                tag='br'
            elif 'mw_t_sx' in element_class: # Uppercase Link
                tag='sx,' + element['href']
            elif 'a' == element_name: # Normal Links
                tag='a,' + element['href']
            elif 'mw_t_d_link' in element_name: # Link, Appears in snotes
                tag='a,' + element['href']
            elif 'badge' in element_class:
                tag='badge'
            elif 'mdash-silent' in element_class: # Uns elements {
                tag='silent_mdash'
            elif 'd-inline' in element_class:
                tag='arrow_svg'
            elif 'unText' in element_class:
                tag='un_text' # }
            elif 'mw_t_wi' in element_class:  # Vis Elements
                tag='italic'
            elif 'mw_t_it' in element_class:
                tag='italic'
            elif 'mw_t_sp' in element_class:
                tag='sp_look_into_this'
            elif 'mw_t_phrase' in element_class:
                tag='bold_italic'
            elif 'note-txt' in element_class: # Supplemental Note
                tag='note_txt'
            elif 'cat' in element_class: # Called Also Text
                tag='cat'
            elif 'cxl' in element_class: # Cognate Cross-References
                tag='cxl'
            elif 'cxt' in element_class:
                tag='a,' + element['href']
            elif 'if' in element_class:
                tag='if'
            elif 'vi' in element_class: # TODO: expand vi elements in uns
                tag='vis'
            elif "dx-jump" in element_class:
                tag = 'dx_jump'
                value = []
                for child_element in element:
                    if not child_element.name:
                        if child_element.text.strip(): # Add non-empty text
                            child_value = custom_strip(child_element.text)
                            value.append(['text', child_value])
                        continue
                    elif 'svg' == child_element.name:
                        value.append(['arrow_svg', ''])
                    elif 'a' == child_element.name:
                        child_tag = 'a,' + child_element['href']
                        value.append([child_tag, child_element.text])

        return [tag, value]
    
    iterate_dictionary_entries()
    json_output = json.dumps(json_list, indent=2)
    return json_output
    
def process_files(input_dir, output_dir):
    """Processes files from the input directory and saves results in the output directory."""
    error_list = []
    for root, _, filenames in os.walk(input_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                input_filepath = os.path.join(root, filename)
                output_filepath = input_filepath.replace(input_dir, output_dir, 1).replace('.html', '.json')

                try:
                    # Create output directory if it does not exist.
                    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)

                    result = parseFile(root, filename)  # Run your parseFile function here
                    
                    # Save the result to a JSON file
                    with open(output_filepath, 'w') as output_file:
                        # json.dump(result, output_file)
                        output_file.write(result)
                    
                except Exception as e:
                    error_list.append([input_filepath, e])
                    print(f"Error processing {input_filepath}: {e}")
    
    json_errors = json.dumps(error_list, indent=2)
    js_file_path1 = os.path.join('word_lists', 'errors2.js')
    with open(js_file_path1, 'w') as js_file:
        js_file.write(json_errors)

def main():
    start_time = datetime.now()

    raw_dictionary_path = 'wimple.html'
    first_letter = raw_dictionary_path[:1]
    first_two_letters = raw_dictionary_path[:2]
    raw_dictionary_dir = 'abridged_dictionary/' + first_letter + '/' + first_two_letters

    src_dir = 'abridged_dictionary'

    print(f"Script started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    process_files(src_dir, 'json_dictionary') # Loop through raw_dictionary
    end_time = datetime.now()
    print(f"Script ended at {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total execution time: {end_time - start_time}")

    # Write to example file
    example_run = parseFile(raw_dictionary_dir, raw_dictionary_path)
    word_lists_dir = 'word_lists'
    js_file_path1 = os.path.join(word_lists_dir, 'example_run.js')
    with open(js_file_path1, 'w') as js_file:
        js_file.write(example_run)

if __name__ == '__main__':
    main()