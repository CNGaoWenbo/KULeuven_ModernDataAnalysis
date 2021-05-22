# -*- coding: utf-8 -*-
"""
Created on Sat May  8 18:06:01 2021

@author: jordan
"""

import os
import pathlib
import glob
import csv
from collections import defaultdict

class FileCsvExport:
    """Generate a CSV file containing the name and contents of all files found"""
    def __init__(self, directory: str, output: str, header = None, file_mask = None, walk_sub_dirs = True, remove_file_extension = True):
        self.directory = directory
        self.output = output
        self.header = header
        self.pattern = '**/*' if walk_sub_dirs else '*'
        if isinstance(file_mask, str):
            self.pattern = self.pattern + file_mask
        self.remove_file_extension = remove_file_extension
        self.rows = 0

    def export(self) -> bool:
        """Return True if the CSV was created"""
        return self.__make(self.__generate_dict())

    def __generate_dict(self) -> defaultdict:
        """Finds all files recursively based on the specified parameters and returns a defaultdict"""
        csv_data = defaultdict(list)
        for file_path in glob.glob(os.path.join(self.directory, self.pattern),  recursive = True):
            path = pathlib.Path(file_path)
            if not path.is_file():
                continue
            content = self.__get_content(path)
            name = path.stem if self.remove_file_extension else path.name
            csv_data[name].append(content)
        return csv_data

    @staticmethod
    def __get_content(file_path: str) -> str:
        with open(file_path) as file_object:
            return file_object.read()

    def __make(self, csv_data: defaultdict) -> bool:
        """
        Takes a defaultdict of {k, [v]} where k is the file name and v is a list of file contents.
        Writes out these values to a CSV and returns True when complete.
        """
        with open(self.output, 'w', newline = '') as csv_file:
            writer = csv.writer(csv_file, quoting = csv.QUOTE_ALL)
            if isinstance(self.header, list):
                writer.writerow(self.header)
            for key, values in csv_data.items():
                for duplicate in values:
                    writer.writerow([key, duplicate])
                    self.rows = self.rows + 1
        return True
import pandas as pd
import numpy
import re
import pycountry

import nltk

import nltk.stem
from nltk.tokenize import word_tokenize, sent_tokenize, PunktSentenceTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation

from gensim.corpora import Dictionary
from gensim.models import LdaModel
from gensim.models import ldaseqmodel
#from gensim.corpora import Dictionary
from gensim.matutils import hellinger

import pyLDAvis
import pyLDAvis.gensim_models as gensimvis

#to plot inside the document
#%matplotlib inline
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def preprocess(data):
    # split country code, session, year
    data[['Country Code', 'Session', 'Year']] = data['File Name'].str.split('_', expand=True)
    
    # add column for full country name
    country_name = []
    for code in data['Country Code']:
        try:
            country_name.append(pycountry.countries.lookup(code).name)
        except LookupError:
            country_name.append('')
    data['Country Name'] = country_name
    
    data[['Session', 'Year']] = data[['Session', 'Year']].apply(pd.to_numeric)
    data = data.astype({"Session": int, "Year": int})
    
    # convert text data to lower case (for easier analysis)
    #data['Content'] = data['Content'].str.lower() #.map(lambda x: re.sub('\W+',' ', x))
    
    column_names = ['File Name', 'Country Code', 'Country Name', 'Session', 'Year', 'Content']
    data = data.reindex(columns=column_names)
    
    # create a unique ID for index
    data['ID'] = range(0, len(data.index))
    data = data.set_index('ID')
    return data
# define paragraoh tokenizer
class SentenceTokenizer(PunktSentenceTokenizer):
    pass


class ParagraphTokenizer(object):
    """A simple paragraph tokenizer that creates a paragraph break whenever
    the newline character appears between two sentences."""

    sentence_tokenizer = SentenceTokenizer()

    def span_tokenize(self, text):
        '''Returns a list of paragraph spans.'''
        sentence_spans = list(self.sentence_tokenizer.span_tokenize(text))
        breaks = []
        for i in range(len(sentence_spans) - 1):
            sentence_divider = text[sentence_spans[i][1]: \
                sentence_spans[i+1][0]]
            if '\n' in sentence_divider:
                breaks.append(i)
        paragraph_spans = []
        start = 0
        for break_idx in breaks:
            paragraph_spans.append((start, sentence_spans[break_idx][1]))
            start = sentence_spans[break_idx+1][0]
        paragraph_spans.append((start, sentence_spans[-1][1]))
        return paragraph_spans
# text cleaning, remove unusual symbols from the text, creating new text_clean column

# convert text data to lower case (for easier analysis)


def clean(s):    
    # Remove any tags:
    cleaned = re.sub(r"(?s)<.?>", " ", s)
    # Keep only regular chars:
    cleaned = re.sub(r"[^A-Za-z0-9(),*!?\'\`]", " ", cleaned)
    # Remove unicode chars
    cleaned = re.sub("\\\\u(.){4}", " ", cleaned)
    return cleaned.strip()

def getFreq(debates_paragraphs):
    # get frequencies by year
    
    freqs = {}
    for i, speech in debates_paragraphs.iterrows():
        year = speech['Year']
        for token in speech['clean']:
            if token not in freqs:
                freqs[token] = {"total_freq":1, year:1}
            else:
                freqs[token]["total_freq"] += 1
                if not freqs[token].get(year):
                    freqs[token][year] = 1
                else:
                    freqs[token][year] += 1
    freqs_df = pd.DataFrame.from_dict(freqs, orient='index')
    freqs_df['word'] = freqs_df.index
    new_cols = ["total_freq", "word"] + sorted(freqs_df.columns.tolist()[1:-1])
    freqs_df = freqs_df[new_cols]

    freqs_df = freqs_df.sort_values('total_freq', ascending=False)
    return freqs_df
    