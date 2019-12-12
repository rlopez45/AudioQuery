#deprecated code

    '''
    [DEPRECATED]
    Gives a similarity score for a string compared to a body of strings
    input:
    token - similarity score to be computed for this string
    d - dictionary whose keys are the body of strings that will compared to string
    returns:
    float - [0, 1]
    '''
    def similarityOld(self,d, string):
        similarities = [(self.mlModel.similarity('string', key)) for key in d]
        return max(similarities)
    delimiters = '_|,\/.?()'
    '''
    [DEPRECATED]
    Check if a word is in the word embedding's vocab
    input:
    word - string (single token should have no delimiters)
    returns:
    result - bool
    '''
    def inVocabOld(self, word):
        return word in self.mlModel.vocab
#modelFilename = 'GoogleNews-vectors-negative300.bin' oldfilename
