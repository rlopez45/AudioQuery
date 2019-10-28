import nltk
import gensim
from nltk.corpus import stopwords as sWords
class SimilarityModule(object):
    modelFilename = 'GoogleNews-vectors-negative300.bin'
    stopwords = set(sWords.words('english'))
    '''
    Instantiates a SimilarityModule 
    input:
    dataObj - dataObject that contains pandas df and parsed audio data
    returns:
    SM object
    '''
    def __init__(self,dataObj):
        self.dataObj = dataObj
        self.mlModel = gensim.models.KeyedVectors.load_word2vec_format(\
            SimilarityModule.modelFilename, binary=True)
    '''
    Makes a list of tuples in the form of (token and part of speech ->
    ('n' - noun, 'v'- verb, 'a'-adjective ...))
    input:
    string- to be tokenized
    returns:
    list -> [(token, part of speech),...]
    '''
    def tokenize(self, string):
        s = string.lower()
        tokens = nltk.word_tokenize(s)
        print(tokens)
        final = nltk.pos_tag(tokens)
        return final
    '''
    Gives a similarity score for a string compared to a body of strings
    input:
    token - similarity score to be computed for this string
    d - dictionary whose keys are the body of strings that will compared to string
    returns:
    float - [0, 1]
    '''
    def similarity(self,d, string):
        similarities = [(self.mlModel.similarity('string', key)) for key in d]
        return max(similarities)
    '''
    Selects the SQL Command that is most similar to a given string
    input:
    string - user provided audio
    returns:
    ids - list of ids - id maps to a SQL Command
    '''
    def SQLSuggestions(self,string):
        pass

if __name__ == "__main__":
    ob = SimilarityModule(None)
    #design test for similarity for the first column and first transformation
    #Give me the total amount of receipts
    inputAudio = 'Give me the total amount of receipts'
    tokens = ob.tokenize(inputAudio)
    print(tokens)
    
