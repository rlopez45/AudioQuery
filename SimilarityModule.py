import nltk
from nltk.corpus import stopwords as sWords
from nltk.corpus import wordnet
import pandas as pd
import time
import re
from SimilarityObjectClass import *
from similarityHelper import *
import dbHelper as dbHelper
import SQLModule as sm

class SimilarityModule(object):
    stopwords = set(sWords.words('english'))
    sqlFilename = "SupportedSQLCommands.txt"

    # Instantiates a SimilarityModule 
    # input:
    #   dataObj - dataObject that contains pandas df and parsed audio data
    # returns:
    #   SM object
    def __init__(self,columns,databaseName):
        self.columns = SimilarityObject(columns)
        sqlTokens = parseSQL(SimilarityModule.sqlFilename)
        self.SQLCommands = SimilarityObject(sqlTokens, 2)
        self.databaseName = databaseName
        self.mlModel = wordnet
            
    # Makes a list of tuples in the form of (token and part of speech ->
    # ('n' - noun, 'v'- verb, 'a'-adjective ...))
    # input:
    #   string - to be tokenized
    # returns:
    #   list - [(token, part of speech),...]
    def tokenize(self, string, stop_words = False):
        s = string.lower()
        tokens = nltk.word_tokenize(s)
        #remove stop words
        if not stop_words:
            tokens = [token for token in tokens if token not in SimilarityModule.stopwords]
        final = nltk.pos_tag(tokens)
        return final

    # returns the most similar word from a dictionary in the form of {word: set(word's synsets)}
    # input:
    #   string - single token
    #   d - dictionary
    # returns:
    #   result most similar iterable in d as compared to its value synonyms
    def mostSimilar(self, d, token, sqlCommandSimilarity = False, test = 1):
        if token == None:
            return None
        if token in d:
            return token

        # assign threshold similarity score
        if sqlCommandSimilarity:
            thresholdSimilarityScore = 0.75
        else:
            thresholdSimilarityScore = 0.5
        print( 'Threshold Similarity Score: ', thresholdSimilarityScore )

        # Find similarity in terms of meaning
        syns = self.mlModel.synsets(token.lower())
        bestScore = None
        best = None
        # if test == 2:
        #     print('token: ', token)
        #     print('d:', d.d)
        #     print('syns: ', syns)
        for string in d:
            synVals = d[string]
            similarityScores = set((syn1.wup_similarity(syn2) for syn1 in syns for syn2 in synVals))
            # if test == 2:
            #     print( "similarityScores: ", similarityScores )
            #     for syn1 in syns:
            #         for syn2 in synVals:
            #             print("syn1: ", syn1, "syn2: ", syn2, "score: ", syn1.wup_similarity(syn2))
            if None in similarityScores:
                similarityScores.remove(None)
            if len(similarityScores) == 0:
                continue
            similarityScore = max(similarityScores)
            if bestScore == None:
                bestScore = similarityScore
                best = string
            else:
                if bestScore < similarityScore:
                    bestScore = similarityScore
                    best = string
        # if test == 2:
        #     print("bestScore: ", bestScore)
        if bestScore == None:
            print('None of the wordnet synonyms for columnnames matched with {}!'.format(token))
            return None
        if bestScore < thresholdSimilarityScore:
            return None
        else:
            return best
    
    # Given the list of noun tokens, construct possible where clauses
    def constructWhereCondition( self, list_of_tokens, dbHelper ):
        # Find where columns in the input token list
        whereCols = set()
        whereTokenToColMap = {}
        for token, pos in list_of_tokens:
            if( token in self.columns ):
                whereCols.add( token )
                whereTokenToColMap[ token ] = token
            else:
                mostSimColumn = self.mostSimilar(self.columns, token)
                if( mostSimColumn != None ):
                    whereCols.add( mostSimColumn ) 
                whereTokenToColMap[ token ] = mostSimColumn
        print( 'whereCols:', whereCols ) 
        print( 'whereTokenToColMap: ', whereTokenToColMap )

        # For each where column, find corresponding value
        # To Do: Update the below to use a better method
        columnTypeMap = dbHelper.getColumnTypes()
        whereColumnToValueMap = {}
        for whereCol in whereCols:
            whereColValues = []
            uniqValues = dbHelper.getUniqueColumnValues( whereCol )
            print('uniqValues: ', uniqValues)
            if( len( uniqValues ) != 0 ):
                print(type(uniqValues[0]))
                print('yo')
                for token, pos in list_of_tokens:
                    mostSimColumnValue = self.mostSimilar( SimilarityObject(uniqValues), token )
                    whereColValues.append( mostSimColumnValue )
            whereColValues = list( set( whereColValues ) )
            whereColValues = [ i for i in whereColValues if i ]
            whereColumnToValueMap[ whereCol ] = whereColValues
        print(whereColumnToValueMap)

        # For each column, find corresponding condition
        whereColumnToConditionMap = {}
        for whereCol in whereCols:
            conditions = []
            colType = columnTypeMap[ whereCol ]
            if( len(whereColumnToValueMap[ whereCol ]) > 0 ):
                # if( colType == 'object'): # To Do: Handle float int and object separately
                    if( len( whereColumnToValueMap[ whereCol ] ) == 1):
                        conditions.append( '=' )
                    else:
                        conditions.append( 'in' )
            whereColumnToConditionMap[ whereCol ] = conditions
        print( "whereColumnToConditionMap: ", whereColumnToConditionMap )

        whereClause = {
            'whereColumns': whereCols, # superset of all columns in the input query, including group by, aggreagtion and non-agg columns
            'whereTokenToColMap': whereTokenToColMap,
            'whereColumnToValueMap': whereColumnToValueMap,
            'whereColumnToConditionMap': whereColumnToConditionMap
        }
        print('Where Clause: ',  whereClause )
        return whereClause

    def constructGroupByClause( self, list_of_tokens ):
        group_by_noun = findGroupByClause(list_of_tokens)
        print( 'group_by_noun: ', group_by_noun )
        group_by_col = None
        if group_by_noun != None:
            group_by_col = self.mostSimilar(self.columns, group_by_noun[0])
        print( 'group_by_col: ', group_by_col)
        groupByClause = {
            'groupByNoun': [ group_by_noun ],   # actual token in the input text
            'groupByCol': [ group_by_col ]      # corresponding translated column
        }
        print( 'groupByClause: ', groupByClause )
        return groupByClause

    def constructAggregationClause( self, remainingNouns, whereClause  ):
        sqlCommands = set()
        sqlNouns    = set()
        whereTokenToColMap = whereClause[ 'whereTokenToColMap' ]
        aggregationCommandToColumnMap = {}
        # print('self.SQLCommands: ', self.SQLCommands.d)
        prevAggCommand = None
        for noun, pos in remainingNouns:
            aggCommand = self.mostSimilar(self.SQLCommands, noun, True)
            print("Current Aggregation Command: ", aggCommand)
            # if the token is not the aggCommand, it is most possibly the column associated with the aggCommand
            if aggCommand is None: 
                if whereTokenToColMap.get( noun, None ) != None:
                    if prevAggCommand == None:  # this token is the first token or 
                        continue                # an agg command has not be encountered yet
                    else:
                        aggregationCommandToColumnMap[ whereTokenToColMap[ noun ] ] = prevAggCommand
                else:   # if token is neither an agg command or column, ignore
                    continue
            else:
                prevAggCommand = aggCommand
            # Store values
            if aggCommand is not None:
                sqlCommands.add(aggCommand)
                sqlNouns.add(noun)
        print('sqlNouns:   ', sqlNouns)
        print('sqlCommands:', sqlCommands)
        print( 'aggregationCommandToColumnMap: ', aggregationCommandToColumnMap)
        return {
            'sqlNouns': sqlNouns,
            'sqlCommands': sqlCommands,
            'aggregationCommandToColumnMap': aggregationCommandToColumnMap
        }

    # Selects the SQL Command that is most similar to a given string
    # input:
    #   string - text in natural language
    # returns:
    #   object: JSON object of features that map to different parts of an SQL command
    def SQLSuggestion(self, string, dbHelper):
        # Tokenize
        all_tokens = self.tokenize(string,True) # with stopwords
        all_tokens_without_sw = self.tokenize(string, False)   # without stopwords
        nouns_without_sw = getNouns(all_tokens_without_sw)
        print('all_tokens: ', all_tokens)
        print('all_tokens_without_sw: ', all_tokens_without_sw)
        print('1. **********nouns without sw: ', nouns_without_sw)

        # Find where condition 
        print('\n\nConstructing where clause...')
        whereClause = self.constructWhereCondition( nouns_without_sw, dbHelper )
        
        # Find group by column
        print('\n\nConstructing Group By clause...')
        groupByClause = self.constructGroupByClause( all_tokens )

        # Remaining nouns after removing repititions and groupByNoun 
        # Using a loop to preserve order
        print('\n\nComputing Remaining nouns (ordered)...')
        remainingNouns = []
        for noun in nouns_without_sw:
            if not (noun in remainingNouns or noun in groupByClause[ 'groupByNoun' ]):
                remainingNouns.append( noun )
        nouns = remainingNouns
        print('Remaining Nouns:', remainingNouns)

        # Construct aggregation clause by associating columns with aggregation functions  
        print('\n\nConstructing Aggregation columns clause...')
        aggClause = self.constructAggregationClause( remainingNouns, whereClause )

        #  process select columns, which can be parameters to aggregation functions also
        print('\n\nConstructing SELECT columns clause...')
        selectColumns = set()
        for noun, pos in nouns:
            if noun in aggClause['sqlNouns']:
                continue
            col = self.mostSimilar(self.columns, noun)
            selectColumns.add(col)
        selectColumns = [i for i in list(selectColumns) if i]
        print("Select columns: ", selectColumns) # will have where and group by columns = all cols, except agg column
        
        # Create an SQL Module object
        sqlObj = {
            'selectColumns': selectColumns, # all cols, except agg column
            'aggregationColumns': list(aggClause[ 'aggregationCommandToColumnMap' ].keys()),
            'aggregationCommandToColumnMap': aggClause[ 'aggregationCommandToColumnMap' ],
            'datasetName': 'data',
            'whereColumnNames': whereClause[ 'whereColumns' ],
            'whereColumnNameToValueMap': whereClause[ 'whereColumnToValueMap' ],
            'whereColumnNameToConditionMap': whereClause[ 'whereColumnToConditionMap' ],
            'groupbyColumns': groupByClause[ 'groupByCol' ],
            'orderbyColumns': [],
            'orderbyColumnToAscDescMap': {}
        }

        print( '\n\nsqlObject: ', sqlObj )
        smObj = sm.SQLModule( sqlObj[ 'selectColumns' ], sqlObj[ 'aggregationColumns' ], sqlObj[ 'aggregationCommandToColumnMap' ],
                        sqlObj[ 'datasetName' ], sqlObj[ 'whereColumnNames' ], sqlObj[ 'whereColumnNameToValueMap' ],
                        sqlObj[ 'whereColumnNameToConditionMap' ], sqlObj[ 'groupbyColumns' ], sqlObj[ 'orderbyColumns' ],
                        sqlObj[ 'orderbyColumnToAscDescMap' ] )
        smObj.formSQLCommand( dbHelper )
        

if __name__ == "__main__":
    # To DO:
    # -- string match for where values ( no need to do synonym match ) --> How will you match numbers, dates ?
    # -- replace value match with actual value
    # -- remove extra where clauses such as: pty_affiliation in 'rep', 'pop', 'ref'

    dfName      = 'data'
    df          = pd.read_csv("data\cand_summary.txt", delimiter = "|")
    dbHelper    = dbHelper.dbHelper( df )
    columns     = dbHelper.getColumnNames()
    ob          = SimilarityModule(columns, dfName)
    # inputString = 'give me the total receipts by affiliation'
    # inputString = 'give me the median of receipts by affiliation'
    # inputString = 'find candidates having candidate id H0AK00055'
    inputString = 'find number of candidates and total receipts by affiliation'
    sqlS        = ob.SQLSuggestion(inputString, dbHelper)
    print(sqlS)