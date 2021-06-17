# -*- coding: utf-8 -*-
"""
Created on Sat May  8 15:28:29 2021

@author: jordan
"""

#import nltk
#nltk.download('wordnet')
#import nltk
#nltk.download('stopwords')
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from string import punctuation
from gensim.models import Phrases
from gensim.corpora.dictionary import Dictionary
from gensim.models import LdaModel
# reomove stop word ( like "is" ,"will" .etc)
stop_words = set(stopwords.words('english'))
stop_words.add("'s")

# The function for clean and format the data
def docs_preprocessor(docs):
    '''Function that conducting tokenize and lemmatize'''
    tokenizer = RegexpTokenizer(r'\w+')
    for idx in range(len(docs)):
        docs[idx] = ''.join(docs[idx])
        docs[idx] = docs[idx].lower()  # Convert to lowercase.
        docs[idx] = tokenizer.tokenize(docs[idx])  # Split into words.

    # Remove numbers, but not words that contain numbers.
    docs = [[token for token in doc if not token.isdigit()] for doc in docs]
    
    # Remove words that are only one character.
    docs = [[token for token in doc if len(token) > 4] for doc in docs]
    
    # Remove stopwords and punctuation.
    docs = [[token for token in doc if not token in stop_words and not token in punctuation] for doc in docs]
    
    # Lemmatize all words in documents.
    lemmatizer = WordNetLemmatizer()
    docs = [[lemmatizer.lemmatize(token) for token in doc] for doc in docs]
  
    return docs
# Perform function on our document
#import warnings
#warnings.filterwarnings("ignore", category=DeprecationWarning)


def docs_biTrigram(docs):
    '''Function that Build Biagram, Trigram  Models '''
    # Add bigrams to docs,minimum count 100 means only that appear 100 times or more.(100,10)
    bigram = Phrases(docs, min_count=100)
    trigram = Phrases(bigram[docs])

    for idx in range(len(docs)):
        for token in bigram[docs[idx]]:
            if '_' in token:
                # Token is a bigram, add to document.
                docs[idx].append(token)
    return docs
def coreModel(docs,no_below=20, no_above=0.8,num_topics=5, chunksize = 800, passes = 20, iterations = 400, eval_every = 1):
    # Create a dictionary representation of the documents.
    dictionary = Dictionary(docs)
    # Filter out words that occur less than 20 documents, no_above 80%
    dictionary.filter_extremes(no_below=20, no_above=0.8)
    #Create dictionary and corpus required for Topic Modeling
    corpus = [dictionary.doc2bow(doc) for doc in docs]
    print('Number of unique tokens: %d' % len(dictionary))
    print('Number of documents: %d' % len(corpus))

      
    
    # Make a index to word dictionary.
    temp = dictionary[0]  # only to "load" the dictionary.
    id2word = dictionary.id2token
    
    #%time 
    lda_model = LdaModel(corpus=corpus, id2word=id2word, chunksize=chunksize, \
                           alpha='auto', eta='auto', \
                           iterations=iterations, num_topics=num_topics, \
                           passes=passes, eval_every=eval_every, random_state=1)

    return dictionary, corpus, lda_model 
#Using c_v Measure
from gensim.models.coherencemodel import CoherenceModel
def compute_coherence_values(dictionary, corpus, texts, limit, start=5, step=5):
    
    #import parallelTestModule
    '''
    if __name__ == '__main__':    
        extractor = parallelTestModule.ParallelExtractor()
        extractor.runInParallel(numProcesses=2, numThreads=4)
    '''
    """
    Compute c_v coherence for various number of topics
    Parameters:
    ----------
    dictionary : Gensim dictionary
    corpus : Gensim corpus
    texts : List of input texts
    limit : Max num of topics

    Returns:
    -------
    model_list : List of LDA topic models
    coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model=LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, random_state=1)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values
import re
import nltk
from nltk.tokenize import word_tokenize
def climateDocsProcess(docs_text):
    # convert text data to lower case (for easier analysis)
    docs_text['text_clean'] = docs_text['Article'].str.lower()
    
    def clean(s):    
        # Remove any tags:
        cleaned = re.sub(r"(?s)<.?>", " ", s)
        # Keep only regular chars:
        cleaned = re.sub(r"[^A-Za-z0-9(),*!?\'\`]", " ", cleaned)
        # Remove unicode chars
        cleaned = re.sub("\\\\u(.){4}", " ", cleaned)
        return cleaned.strip()
    
    # clean text
    docs_text['text_clean'] = docs_text.text_clean.apply(lambda x: clean(x))
    # tockenize text
    docs_text['token'] = docs_text['text_clean'].apply(word_tokenize)
    stop_words = set(stopwords.words('english'))
    #remove  the stop words
    stop_words.add("'")
    stop_words.add("-")
    stop_words.add("'")
    stop_words.add("'s")
    docs_text['clean'] = docs_text['token'].apply(lambda x: [w for w in x if not w in stop_words and not w in punctuation])
    lemm = nltk.WordNetLemmatizer()
    docs_text['lemm'] = [[format(lemm.lemmatize(token)) for token in speech] for speech in docs_text['clean']]# lemmatize the doc
    
    text_climate = docs_text[docs_text['Article'].str.contains("climate")] #choose the Doc which contain the "climate"
    texts_climate = text_climate['lemm']
    # Remove words that less than 3 characters.
    texts_climate = [[token for token in text if len(token) > 3] for text in texts_climate]
    # Remove numbers, but not words that contain numbers.
    texts_climate = [[token for token in text if not token.isdigit()] for text in texts_climate]
    # Includes biagram models
    return texts_climate