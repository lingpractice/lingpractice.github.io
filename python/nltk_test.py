from nltk.corpus import brown
from nltk.corpus import words
from nltk import FreqDist
import json

# Generate the frequency distribution
brown_words = [word.lower() for word in brown.words()]
fdist = FreqDist(brown_words)

# Frequency Distribution
most_common_words = fdist.most_common()
filtered_words = [(word, freq) for word, freq in most_common_words if len(word) >= 4 and word.isalpha()]
# js_array_str = '[\n' + ',\n'.join([f"  {{word: '{word}', frequency: {freq}}}" for word, freq in filtered_words]) + '\n]'
js_array_str = '[\n' + ',\n'.join([f"  '{word}'" for word, freq in filtered_words]) + '\n]'
js_array_str = f"const wordFrequency = {js_array_str};\n"
with open('wordFrequency.js', 'w') as js_file:
    js_file.write(js_array_str)

# Word List 
word_list = list(set(words.words()))
word_list.sort()
filtered_words = [(word) for word in word_list if len(word) >= 4 and word.isalpha()]
# filtered_words = [(word) for word in word_list]
print(len(word_list))
print(len(filtered_words))
word_list_str = '[\n' + ',\n'.join([f"  '{word}'" for word in filtered_words]) + '\n]'
word_list_str = f"const fullWordList = {word_list_str};\n"
with open('wordList.js', 'w') as js_file:
    js_file.write(word_list_str)
