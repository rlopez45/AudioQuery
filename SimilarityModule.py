import nltk
from nltk.corpus import stopwords as sWords
from nltk.corpus import wordnet
import pandas as pd
import time
import re
from SimilarityObjectClass import *
from similarityHelper import *

class SimilarityModule(object):
    stopwords = set(sWords.words('english'))
    sqlFilename = "SupportedSQLCommands.txt"
    '''
    Instantiates a SimilarityModule 
    input:
    dataObj - dataObject that contains pandas df and parsed audio data
    returns:
    SM object
    '''
    def __init__(self,columns,databaseName):
        self.columns = SimilarityObject(columns)
        sqlTokens = parseSQL(SimilarityModule.sqlFilename)
        self.SQLCommands = SimilarityObject(sqlTokens)
        self.databaseName = databaseName
        self.mlModel = wordnet
            
    '''
    Makes a list of tuples in the form of (token and part of speech ->
    ('n' - noun, 'v'- verb, 'a'-adjective ...))
    input:
    string- to be tokenized
    returns:
    list -> [(token, part of speech),...]
    '''
    def tokenize(self, string, stop_words = False):
        s = string.lower()
        tokens = nltk.word_tokenize(s)
        #remove stop words
        if not stop_words:
            tokens = [token for token in tokens if token not in SimilarityModule.stopwords]
        final = nltk.pos_tag(tokens)
        return final
    
    
    '''
    returns the most similar word from a dictionary in the form of {word: set(word's synsets)}
    input:
    string - single token
    d - dictionary
    returns:
    result most similar iterable in d as compared to its value synonyms
    '''
    def mostSimilar(self, d, string):
        if string == None:
            return None
        #heuristic check for exact match
        if string in d:
            return string
        syns = self.mlModel.synsets(string.lower())
        bestScore = None
        best = None
        for string in d:
            synVals = d[string]
            similarityScores = set((syn1.wup_similarity(syn2) for syn1 in syns for syn2 in synVals))
            if None in similarityScores:
                similarityScores.remove(None)
            if len(similarityScores) == 0:
                continue
            similarityScore = max(similarityScores)
            if bestScore == None:
                bestScore = similarityScore
                best = string
            else:
                if bestScore<similarityScore:
                    bestScore = similarityScore
                    best = string
        if bestScore == None:
            print('there were no tokens in input dictionary that can be found in wordnet')
            return None
        if bestScore<.5:
            return None
        return best
    
    '''
    Selects the SQL Command that is most similar to a given string
    input:
    string - user provided audio
    returns:
    ids - list of ids - id maps to a SQL Command
    '''
    def SQLSuggestion(self,string):
        full_tokens = self.tokenize(string,True)
        no_stop = self.tokenize(string, False)
        nouns = getNouns(no_stop)
        group_by_noun = findForEach(full_tokens)
        group_by_col = None
        if group_by_noun!=None:
            group_by_col = self.mostSimilar(self.columns, group_by_noun[0])
        nouns_no_repeats = []
        noun_set = set()
        for noun in nouns:
            if noun_set not in noun_set:
                nouns_no_repeats.append(noun)
                noun_set.add(noun)
        nouns = nouns_no_repeats
        if group_by_noun in nouns:
            nouns.remove(group_by_noun)
        #process sql commands
        sqlCommands = set()
        sqlNouns = set()
        for tuple in nouns:
            noun,x = tuple
            command = self.mostSimilar(self.SQLCommands, noun)
            if command in sqlCommands:
                continue
            if len(sqlCommands)<2:
                sqlCommands.add(command)
                sqlNouns.add(noun)
            else:
                break
        #process columns
        cols = set()
        for tuple in nouns:
            noun, x = tuple
            if noun in sqlNouns:
                continue
            col = self.mostSimilar(self.columns, noun)
            r = str(noun) + str(col)
            cols.add(col)
        sqlString = 'SELECT '
        columnString = ''
        if len(cols)>1:
            columnString = ','.join(cols)
        else:
            col = list(cols)[0]
            columnString = col
        dataFrameString = "FROM " + self.databaseName
        group_by = ''
        if group_by_noun !=None:
            group_by = 'GROUP_BY {}'.format(group_by_col)
        return sqlString + columnString+ " " + dataFrameString +" " +  group_by 
        

if __name__ == "__main__":
    start = time.time()
    dataFrameName = 'data'
    df = pd.read_csv("data\cand_summary.txt", delimiter = "|")
    columns = list(df.columns)
    ob = SimilarityModule(columns, dataFrameName)
    end = time.time()
    print(end-start)
    result = ob.mostSimilar(ob.columns, 'receipts')
    inputString = 'give me the total receipts for each affiliation'
    sqlS = ob.SQLSuggestion(inputString)
    print(sqlS)
    
    
