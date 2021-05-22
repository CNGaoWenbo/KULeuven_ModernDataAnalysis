# -*- coding: utf-8 -*-
"""
Created on Sat May  8 17:30:12 2021

@author: jordan
"""
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer

# To tokenize the data,use CountVectorizer
# Calling our overwritten Count vectorizer
lemm = WordNetLemmatizer()
class LemmaCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(LemmaCountVectorizer, self).build_analyzer()
        return lambda doc: (lemm.lemmatize(w) for w in analyzer(doc))
    
def readFileTF(path = "../data/output.csv"):
    # Read the CSV file that include the 8093 documents.
    docs_text = pd.read_csv(path)
    docs_text = docs_text['Content']
    
    # Remove numbers, but not words that contain numbers.
    docs_text = [x for x in docs_text if not (x.isdigit() 
                                             or x[0] == '-' and str(x[1:]).isdigit())]
    docs_text=pd.DataFrame(docs_text,columns=['Article'])
    return docs_text