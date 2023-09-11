import os
from gensim.models.ldamodel import LdaModel
from gensim.utils import simple_preprocess
import pyLDAvis.gensim_models as gensimvis
import pyLDAvis

path = r"C:\Users\balog\Desktop\Scrape1"
text = ""

for filename in os.listdir(path):
    if filename.endswith('.txt'):
        with open(os.path.join(path, filename), 'r', encoding='utf-8') as file:
            text += file.read()

try:
    # Tokenize the text
    tokens = simple_preprocess(text)
    # Create a dictionary from the tokenized documents
    dictionary = corpora.Dictionary([tokens])
    # Create the corpus from the tokenized documents
    corpus = [dictionary.doc2bow(tokens)]
    print(corpus)
    # Build the LDA model
    if corpus:
        lda_model = LdaModel(corpus=corpus,
                             id2word=dictionary,
                             num_topics=5,
                             random_state=100,
                             update_every=1,
                             chunksize=100,
                             passes=10,
                             alpha=10000,
                             per_word_topics=True)
        # Visualize the topics
        vis = gensimvis.prepare(lda_model, corpus, dictionary)
        pyLDAvis.save_html(vis, 'Origo_2011_nemzeti.html')
except TypeError:
    pass