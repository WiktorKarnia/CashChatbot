import nltk
from nltk.stem.porter import PorterStemmer
import numpy as np
from pystempel import Stemmer
from langdetect import detect

polish_stemmer = Stemmer.default()
english_stemmer = PorterStemmer()

def tokenize(sentence, language):
    if language == 'polish':
        return nltk.word_tokenize(sentence, language='polish')
    else:
        return nltk.word_tokenize(sentence, language='english')

def stem(word, language):
    if language == 'polish':
        return polish_stemmer(word.lower())
    else:
        return english_stemmer.stem(word.lower())

def bag_of_words(tokenized_sentence, all_words, language):
    tokenized_sentence = [stem(word, language) for word in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for index, word in enumerate(all_words):
        if word in tokenized_sentence:
            bag[index] = 1.0
    return bag

def detect_language(text):
    if not text or len(text) < 3:
        return 'unknown'
    
    try:
        lang = detect(text)
        if lang == 'pl':
            return 'polish'
        else:
            return 'english'
    except:
        return 'unknown'
