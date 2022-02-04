import csv
import pandas as pd
import time
import os
import psutil
start = time.time()


def remove_special_characters(word):
    only_alpha = ""

    for char in word:

        if ord(char) >= 65 and ord(char) <= 90:
            only_alpha += char
        elif ord(char) >= 97 and ord(char) <= 122:
            only_alpha += char
        elif len(only_alpha) > 1:
            break
    return only_alpha


with open('find_words.txt', 'r') as find_words:
    find_words_list = []

    for line in find_words:
        find_words_list.append(line.strip())

french_dictionary_df = pd.read_csv('french_dictionary.csv')

# get english words
english_list = []
for i in french_dictionary_df.iloc[:, 0]:
    english_list.append(str(i))

# French list
french_list = []
for i in french_dictionary_df.iloc[:, 1]:
    french_list.append(str(i))

# Forming a translation dictionary
translations_dict = {}
for eng_word in english_list:
    for french_word in french_list:
        # Making sure only words whose translation is available are taken into account
        if eng_word in find_words_list:
            translations_dict[eng_word] = french_word
        french_list.remove(french_word)
        break

# working on the text file contents

translated_words = {}

with open('t8.shakespeare.txt', 'r+') as shakespere:
    updated_elements = []
    for individual_line in shakespere:
        split_line = individual_line.split(' ')
        index = 0

        for word in split_line:

            last_word = False
            punc = ''
            if '\n' in word:
                word = word[:-1]
                last_word = True
            whole_word = str(word)
            word = remove_special_characters(word)
            prefix = ''
            sufix = ''
            if len(whole_word) > len(word):
                start_index = whole_word.find(word)
                end_index = whole_word.find(word) + len(word)
                prefix = whole_word[:start_index]
                sufix = whole_word[end_index:]

            if len(word) != 0 and (word.lower() in translations_dict):

                if word.isupper():
                    if last_word:
                        split_line[index] = prefix+str(
                            (translations_dict[word.lower()]).upper()) + sufix + '\n'
                    else:
                        split_line[index] = prefix+(
                            translations_dict[word.lower()]).upper()+sufix

                elif word[0].isupper():
                    if last_word:
                        split_line[index] = prefix+str(
                            (translations_dict[word.lower()]).capitalize()) + sufix + '\n'
                    else:
                        split_line[index] = prefix+(
                            translations_dict[word.lower()]).capitalize()+sufix
                else:
                    if last_word:
                        split_line[index] = prefix+str(
                            translations_dict[word.lower()]) + sufix + '\n'
                    else:
                        split_line[index] = prefix + \
                            translations_dict[word.lower()] + sufix

                if word.lower() in translated_words:

                    translated_words[word.lower()] = int(
                        translated_words[word.lower()]) + 1
                else:
                    translated_words[word.lower()] = 1

            index += 1
        updated_elements.append(split_line)

# Wriring to input file:
open('t8.shakespeare.txt', 'w').close()

with open('t8.shakespeare.txt', 'w') as textfile:
    for single_line_list in updated_elements:
        textfile.write(' '.join(single_line_list))

end = time.time()
print('List of translated words: \n', list(translated_words.keys()))
print('Occurence of each word: \n', translated_words)
print(f"Runtime of the program is {end - start}")
print(
    f'Memory used by program: {psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2} MB')

# csv frequency writing:
with open("frequency.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(['English word', 'French word', 'Frequeny'])
    for eng_word in translated_words:
        writer.writerow([
            eng_word, translations_dict[eng_word], translated_words[eng_word]])
