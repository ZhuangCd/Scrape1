import json
import os
import spacy
import time

start_time = time.time()

nlp = spacy.load('hu_core_news_lg')

words1 = [
    'magyar',
    'magyarok',
    'magyaros',
    'magyarság',
    'magyarország',
    'magyarországi',
    'magyarországiak',
    'magyarországon',
    'nemzet',
    'nemzeti',
    'Magyar',
    'Magyarok',
    'Magyaros',
    'Magyarság',
    'Magyarország',
    'Magyarországi',
    'Magyarországiak',
    'Magyarországon',
    'Nemzet',
    'Nemzeti',
    'nemzetállam',
    'Nemzetállam']
words2 = [
    'európa',
    'európaiak',
    'európában',
    'európai',
    'Európa',
    'Európaiak',
    'Európában',
    'Európai',
    'kelet-európa',
    'kelet-európai',
    'Kelet-európa',
    'Kelet-európai',
    'nyugat-európa',
    'nyugat-európai',
    'Nyugat-európa',
    'Nyugat-európai',
    'közép-európa',
    'Közép-európa',
    'közép-európai',
    'Közép-európai']

path = r'C:\Users\balog\Desktop\Scrape1'
json_files = [os.path.join(path, file)
              for file in os.listdir(path) if file.endswith('.json')]

nemzeti = set()
europai = set()

texts1 = []
texts2 = []

for file in json_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # ugye a p_tags-ban van a szöveg, de máshol lehet más tagben is
        text = ' '.join(data['p_tags'][1:])
        doc = nlp(text)
        text = ' '.join(
            [token.lemma_ for token in doc if not token.is_stop and token.is_alpha])
        if any(word in text for word in words1):
            text = ''.join(text)
            text = text.replace("\n", "")
            nemzeti.add(text)
            texts1.append(text)
        print(text)
        if any(word in text for word in words2):
            text = ''.join(text)
            text = text.replace("\n", "")
            europai.add(text)
            texts2.append(text)

with open('nemzeti.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(texts1))

with open('europai.txt', 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(texts2))
end_time = time.time()
elapsed_time = end_time - start_time
print("Ennyi idő alatt futott le: {:.2f} másodperc".format(elapsed_time))
print('Na most van kész')