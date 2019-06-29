"""Process documents into sentence vectors."""
from collections import Counter
import numpy as np

common_ngrams = "most_common_ngrams.txt"
with open(common_ngrams, 'r', encoding='utf-8') as f:
    ngram_list = f.readlines()
ngram_list = [x.strip() for x in ngram_list]

min_n = min(len(x) for x in ngram_list)
max_n = max(len(x) for x in ngram_list)

def convert_sentence_to_vec(sentence):
    """Convert text into vector using most common char n-grams.
    
    Count the frequency of each of the n-grams in a sentence
    and create a numpy array of those frequencies.
    
    params: sentence — string
    
    returns: string_vector — numpy array with the vector representation of sentence."""
    sentence_ngrams = []
    string_vector = []
    for n in range(min_n, max_n +1):
        sentence_ngrams.extend([sentence[i:i+n] for i in range(len(sentence)-n+1)])
    counter_ngrams = Counter(sentence_ngrams)
    for ngram in ngram_list:
        if ngram in sentence_ngrams:
            string_vector.append(float(counter_ngrams[ngram]))
        else:
            string_vector.append(0.0)
    string_vector = np.array(string_vector)
    return string_vector
