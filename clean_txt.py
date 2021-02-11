#!/usr/bin/env python
# coding: utf-8

__author__ = 'F.Feenstra'

import nltk
import re                                  
import string  
import spell
from nltk.corpus import stopwords          
#from nltk.stem import PorterStemmer        


def clean(text):
    # lower text
    text = text.lower()
    # remove hyperlinks
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text)
    # remove hashtags
    text = re.sub(r'#', '', text)
    # remove afbreekstreepje
    text = re.sub(r'\n-', '', text)
    return text

def get_keywords(text):
    #tokenize
    tokens = nltk.word_tokenize(text)
    stop_words = stopwords.words('dutch') 
    #remove stopwords and punctiation
    keywords = [word for word in tokens if not word in stop_words and not word in string.punctuation]
    print(f'deze tekst heeft {len(keywords)} aantal woorden')
    return keywords

def get_unknown(keywords):
    unknown = [word for word in keywords if not word in spell.WORDS]
    print(f'{len(unknown)} aantal onbekend')
    return unknown

def stem(keywords):
    stemmer = PorterStemmer() 
    words_stemmed = [stemmer.stem(word) for word in keywords]
    return words_stemmed

def correct(unknown):
    corrected = 


with open('Casestudy.txt') as f:
    text = f.read()
    text = clean(text)
    keywords = get_keywords(text)
    unknown = get_unknown(keywords)
    corrected = [spell.correction(word) for word in unknown]
    corpus = keywords + corrected



