import re
import nltk
from nltk.corpus import wordnet
from website.similarityHelper import *

class SimilarityObject(object):

    '''
    Helper method don't call directly
    Splits a string on a set of delimiters
    Input:
    delimiters      : string where each char is a delimiter
    list_of strings : [(str), (str)...]
    Returns:
    dictionary      : keys = tokens; vals = split tokens on delimiters
    '''
    def splitList(self, list_of_strings, delimiters = '_|,\/.?()'):
        d = {}
        for string in list_of_strings:
            if type( string ) == 'object':
                split = re.split(delimiters, string.lower())
            else:
                split = re.split(delimiters, string)
            split = set(split)
            if None in split:
                split.remove(None)
            d[string] = split
        return d
        
    '''
    Helper method don't call directly
    Transforms a dictionary's values (iterable of strings) into a set of all the vals corresponding synonyms
    Input:
    d             : Dictionary with keys = tokens and vals = split tokens on delimiters
    Returns:
    transformed_d : Dictionary with key = string and val = set of synonyms
    '''
    def getSynonyms(self, d):
        transformed_d = {}
        for string in d:
            new = set()
            split = d[string]
            for s in split:
                syns = wordnet.synsets(s)
                for syn in syns:
                    lemmas = [lemma.name() for lemma in syn.lemmas()]
                new.update(syns)
            transformed_d[string] = new
        return transformed_d

    # Helper Method (dont call directly):
    # Given a list of synonyms, excludes certain synonyms from the list 
    def excludeSynonyms( self, synsList, synsToExcludeList ):
        if( synsToExcludeList == [] or synsToExcludeList == None ):
            return synsList
        synsListResult = [];
        for syn in synsList: 
            if syn not in synsToExcludeList:
                synsListResult.append( syn )
        return synsListResult

    # Find synonyms for sql keywords
    def getSQLKeywordSynonyms(self, sqlKeywordsDict):
        transformed_d = {}
        # Synonyms to exclude for an SQL command if a long list of synonyms are present
        synsToExclude = {
            'sum':    [ wordnet.synset('sum.n.01'), wordnet.synset('kernel.n.03'), wordnet.synset('summarize.v.02') ],
            'sort':   [ wordnet.synset('kind.n.01'), wordnet.synset('sort.n.02'), wordnet.synset('sort.n.03'), wordnet.synset('screen.v.03') ],
            'median': [ wordnet.synset('medial.s.01') ],
            'count':  [ wordnet.synset('count.n.02'), wordnet.synset('count.n.03'), wordnet.synset('count.v.02'), wordnet.synset('consider.v.04'), wordnet.synset('count.v.08'), wordnet.synset('reckon.v.06') ],
        }
        # Custom synonym list to include specified for SQL commands
        synsToInclude = {
            'min'   : [ wordnet.synset('minimum.a.01'), wordnet.synset('minimum.n.01') ],
            'max'   : [ wordnet.synset('maximum.a.01'), wordnet.synset('maximum.n.01'), wordnet.synset('maximum.n.02'),  wordnet.synset('utmost.n.01'), wordnet.synset('maximal.a.01') ]
        }
        for sqlKeyword in sqlKeywordsDict:
            new = set()
            splitSet = sqlKeywordsDict[ sqlKeyword ]
            for s in splitSet:
                if ( len( synsToInclude.get( s, [] )) ):
                    syns = synsToInclude[ s ]
                else:
                    syns = wordnet.synsets(s)
                # NOTE: Doing the below to avoid situations where column names match with sql keywords
                # owing to an unintended meaning of the sql keyword. For e.g. the keyword 'receipts' matches with
                # term wordnet.synset('sum.n.01') with a > 0.9 similarity score, where wordnet.synset('sum.n.01')
                # mean 'a quantity of money'. However for finding synonyms for the SQL keyword SUM, we dont need 
                # to consider certain meanings of sum (in this case, we dont need to consider wordnet.synset('sum.n.01')).
                syns = self.excludeSynonyms( syns, synsToExclude.get(s, []) ) 
                # for syn in syns:
                #     self.getSynonymInfo( syn )                    
                new.update(syns)
            transformed_d[ sqlKeyword ] = new
        return transformed_d

    def getSynonymInfo(self, syn):
        lemmas = [lemma.name() for lemma in syn.lemmas()]
        print("Synonym: ", syn)
        print("Synonym Definition: ", syn.definition())
        print("Associated Lemmas: ", lemmas)

    def __contains__(self, key):
        return key in self.d

    def __iter__(self):
        for key in self.d:
            yield key

    def __getitem__(self, key):
        return self.d[key]

    '''
    list_of_tokens  : Refers to the list of strings for which synonyms are to be found
    token_type      : Refers to the type os strings in the list provided, 
                    e.g. is it a list of SQL keywords or general english words
                    1 = General words; 2 = SQL keywords
    '''
    def __init__(self, list_of_tokens, token_type = 1):
        list_of_tokens_tmp = []
        for i in list_of_tokens:
            if str(i) != 'nan' and i != None:
                if isinstance(i, str) or type(i) == 'object':
                    list_of_tokens_tmp.append(i.lower())
                else:
                    list_of_tokens_tmp.append(i)
        list_of_tokens = list_of_tokens_tmp
        delimiter_d = self.splitList(list_of_tokens)
        if( token_type == 1 ):      # if tokens are general words
            self.d      = self.getSynonyms(delimiter_d)
        if( token_type == 2 ):      # if tokens are SQL keywords
            self.d      = self.getSQLKeywordSynonyms(delimiter_d)

if __name__ == "__main__":
    # print(parseSQL("SupportedSQLCommands.txt"))
    smObject = SimilarityObject(parseSQL("SupportedSQLCommands.txt"), 2)
    # smObject = SimilarityObject(['Total_Receipts', 'party'], 1)
    # print('minimum synsets:', wordnet.synsets('minimum'))
    # for syn in wordnet.synsets('minimum'):
    #     smObject.getSynonymInfo(syn)
    # print('maximum synsets:', wordnet.synsets('maximum'))
    # for syn in wordnet.synsets('maximum'):
    #     smObject.getSynonymInfo(syn)
    
