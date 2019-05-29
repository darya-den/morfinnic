"""Module with morphological analysis."""
import pandas as pd
import numpy
import shelve

affixes = pd.read_csv("upd_affixes_new.csv")

def final_tag(words, lang):
    """Get morphological tags for sentence.

    Split the sentence into words and determone the most probable tags
    for each word with the get_tags method.

    params: sentence -- string
            lang -- string with language code

    return: list with the most probable tag/tags for each word"""
    language_data = affixes[affixes["language"] == lang].to_dict()
    sentence_tags = []
    with shelve.open("stem_counts") as stem_db:
        for word in words:
            tags = get_tags(word, language_data, lang, stem_db)
            sentence_tags.append(tags)
    return sentence_tags


def get_tags(word, affixes, lang, stem_db):
    """Get morphological tags for a word.

    Find all possible affixes for the word. Determine the hypothetical stems
    and find the most probable one (with the highest score).
    The most probable tags are considered to be the ones that correspond
    to the most probable stem.

    params: words — string
            affixes — pandas DataFrame with the affixes of a language
            lang — string with language code
            stem_db — shelve db with the stem counts

    return: list with most probable tag/tags"""
    tags = []
    affix_list = affixes["affix"]
    max_count = 0
    for index in affix_list:
        aff = affix_list[index]
        if not len(aff) >= len(word):
            if aff == "#":
                tag = affixes["meaning"][index]
                stem = word
                try:
                    stem_count = stem_db[lang][stem]
                except KeyError:
                    stem_count = 1
                if stem_count > max_count:
                    max_count = stem_count
                tags.append((aff, tag, stem_count))
            if word.endswith(aff):
                tag = affixes["meaning"][index]
                if ("POS:nomin" in tag) and ("NUMB:" not in tag):
                    tag += "NUMB:sg|"
                if ("POS:nomin" in tag) and ("CASE:" not in tag):
                    tag += "CASE:nom|"
                if ("POS:verb" in tag) and ("TENSE:" not in tag):
                    tag += "TENSE:pres|"
                if lang == "kar" or lang == "veps":
                    if ("POS:verb" in tag) and ("MOOD:" not in tag):
                        tag += "MOOD:ind|"
                if lang == "fin":
                    if ("POS:verb|" in tag) and ("VOICE:" not in tag):
                        tag += "VOICE:act|"
                stem = word[:-len(aff)]
                try:
                    stem_count = stem_db[lang][stem]
                except KeyError:
                    stem_count = 1
                if stem_count > max_count:
                    max_count = stem_count
                tags.append((aff, tag, stem_count))
    if tags != []:
        #print(tags)
        res = []
        for tagset in tags:
            if tagset[2] == max_count:
                res.append(tagset[1])
    else:
        res = ["X"]
    return res
        
