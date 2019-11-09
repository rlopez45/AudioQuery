import re
from nltk.corpus import wordnet
class SimilarityObject(object):
    '''
    [helper method don't call directly]
    Splits a string on a string of delimiters
    input:
    delimiters - string where each char is a delimiter
    list_of strings - [(str), (str)...]
    returns:
    dictionary - tokens - keys , split tokens on delimiters - vals
    '''
    def splitList(self, list_of_strings, delimiters = '_|,\/.?()'):
        d = {}
        for string in list_of_strings:
            split = re.split(delimiters, string.lower())
            split = set(split)
            if None in split:
                split.remove(None)
            d[string] = split
        return d
    '''
    [helper method don't call directly]
    transforms a dictionary's vals (iterable of strings) into a set of
    all the vals corresponding synonyms
    input:
    d - key- string -val iterable of split string on delimiters
    returns:
    transformed_d - key- string , val - set of synonyms
    '''
    def getSynonyms(self, d):
        transformed_d = {}
        for string in d:
            new = set()
            split = d[string]
            for s in split:
                syns = wordnet.synsets(s)
                new.update(syns)
            transformed_d[string]  = new
        return transformed_d
    def __contains__(self, key):
        return key in self.d
    def __iter__(self):
        for key in self.d:
            yield key
    def __getitem__(self, key):
        return self.d[key]
    def __init__(self, list_of_tokens):
        delimiter_d = self.splitList(list_of_tokens)
        self.d = self.getSynonyms(delimiter_d)

if __name__ == "__main__":
    smObject = SimilarityObject(['booty', 'boot'])
