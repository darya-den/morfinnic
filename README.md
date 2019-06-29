# morfinnic
Language Identification and Morphological Analysis for Finnic Languages

## What do you need?
LI is done with the Neural Network and for that you need to install [**Keras**](http://keras.io).

Weights of the model are saved in hdf5, so you need [**h5py**](https://pypi.org/project/h5py/).

**shelve** is necessary for morhological analysis.

Another required Python libraries are [**pandas**](https://pandas.pydata.org) and [**numpy**](https://www.numpy.org).

## How to implement?
Everything you need is in the **analyze.py** file. 

```
from analyze import analyze

text = "..."
print(analyze(text))
```

*analyze* method prints the morphological analysis for the 2 most probable guesses of languages.

## About
**morfinnic** is a thesis project for BA in Computational Linguistics at SPSU.

As of now, **morfinnic** supports only a few POS: nominals (nouns, adjectives, pronouns) and verbs. Morphological disambiguation is not implemented.
