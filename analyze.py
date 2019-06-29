"""Module for joint LI and morphological tagging."""
import tagging
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sentence_vectors import convert_sentence_to_vec
from config import n_languages, language_codes
import re
import operator

# create NN for word-level LI
network_words = Sequential()
network_words.add(Dense(200, input_dim=200, activation='sigmoid'))
network_words.add(Dense(120, activation='sigmoid'))
network_words.add(Dense(60, activation='sigmoid'))
network_words.add(Dense(n_languages, activation='softmax'))

network_words.load_weights('weights_words.hdf5')
network_words.compile(loss='binary_crossentropy',
                      optimizer='sgd', metrics=['accuracy'])

# create LI for sentence-level LI
network = Sequential()
network.add(Dense(200, input_dim=200, activation='sigmoid'))
network.add(Dense(120, activation='sigmoid'))
network.add(Dense(60, activation='sigmoid'))
network.add(Dense(n_languages, activation='softmax'))

network.load_weights('weights.hdf5')
network.compile(loss='binary_crossentropy',
                optimizer='sgd', metrics=['accuracy'])

def predict_lang(n_words, sentence):
    """Predict the language of a text with a Neural Network.
    
    Predict the language of the text using a NN and display the 
    probabilities of all languages.
    
    params: n_words — number of words in a sentence
            sentence — string with the text
            
    returns: lang_labels — 2 most probable languages"""
    v = convert_sentence_to_vec(sentence)
    vct = np.zeros((1, 200))
    for count, digit in enumerate(v):
        vct[0, count] = int(digit)
    if n_words > 1:
        prediction_vct = network.predict(vct)
    else:
        prediction_vct = network_words.predict(vct)
    langs = sorted(language_codes.keys())
    scores = []
    print("The predictions for languages:")
    print()
    for i in range(n_languages):
        lang = langs[i]
        lang_score = round(prediction_vct[0, i]*100, 2)
        scores.append((lang[:-3], lang_score))
        print(lang[:-3] + " : " + str(lang_score))
    scores.sort(key=operator.itemgetter(1), reverse=True)
    lang_labels = scores[0][0] + " " + scores[1][0]
    return lang_labels          

def analyze(sentence):
    """Get all possible tags for the words of the sentence.
    
    Preprocess the sentence, determine 2 most probable languages,
    then get morphological tags of all words.
    
    params: sentence — string wi the text.
    
    returns: None."""
    sentence = sentence.lower()
    sentence = re.sub(r'[«»\:;\,\-\—\—\”\(\)\"\]\[\%\–\“\d\„\&/…@\*]', "", sentence)
    sentence_nn = re.sub(r'[\s]', "_", sentence)
    sentence_nn = re.sub(r'[\.\!\?]', "_", sentence_nn)
    sentence_nn = "_" + sentence + "_"
    words = sentence.split()
    lang_labels = predict_lang(len(words), sentence_nn).split()
    for lang in lang_labels:
        tags = tagging.final_tag(words, lang[:3])
        print()
        print("The results of the analysis for {0}:".format(lang))
        print()
        for n, word in enumerate(words):
            print("Word: {}".format(word))
            print("Possible tags:")
            for tag in tags[n]:
                print(tag)
            print()
