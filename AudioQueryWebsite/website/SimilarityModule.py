import nltk
from nltk.corpus import stopwords as sWords
from nltk.corpus import wordnet
import pandas as pd
import time
import re
from website.SimilarityObjectClass import *
from website.similarityHelper import *
import website.dbHelper as dh
import website.SQLModule as sm
import pprint
pp = pprint.PrettyPrinter(indent = 4)
import website.outputGen as outGen
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

class SimilarityModule(object):
    stopwords = set(sWords.words('english'))
    sqlFilename = dir_path + "\\" + "SupportedSQLCommands.txt"

    def __init__(self, columns, databaseName):
        self.columns = SimilarityObject(columns)
        sqlTokens = parseSQL(SimilarityModule.sqlFilename)
        self.SQLCommands = SimilarityObject(sqlTokens, 2)
        self.databaseName = databaseName
        self.mlModel = wordnet
            
    # Tokenize and tag with Parts of Speech
    # Inputs:
    # string - to be tokenized
    # Output:
    # list of tokens - [(token, part of speech),...]
    def tokenize(self, string, stopwords = False):
        s = string.lower()
        tokens = nltk.word_tokenize(s)
        if not stopwords:
            tokens = [token for token in tokens if token not in SimilarityModule.stopwords]
        final = nltk.pos_tag(tokens)
        return final

    # Returns the most similar word from a dictionary given a word and a dictionary
    # Inouts:
    # token - word whose synonym is to be found
    # d - dictionary in the form of {word: set(word's synsets)}
    # Output:
    # Synonym of token with the highest similarity score 
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
            # if test == 2 and token == 'minimum':
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
        if test == 2:
            print("bestScore: ", bestScore)
        if bestScore == None:
            print('None of the wordnet synonyms for words in the dictionary matched with {}!'.format(token))
            return None
        if bestScore < thresholdSimilarityScore:
            return None
        else:
            return best
    
    def getWhereColumns( self, list_of_tokens, dbHelper ):
        whereCols = set()
        whereTokenToColMap = {}
        for token, pos in list_of_tokens:
            if( token in self.columns ):
                whereCols.add( token )
                whereTokenToColMap[ token ] = token
                list_of_tokens.remove( (token, pos) )
            else:
                mostSimColumn = self.mostSimilar(self.columns, token)
                if( mostSimColumn != None ):
                    whereCols.add( mostSimColumn )
                    whereTokenToColMap[ token ] = mostSimColumn
        print( 'whereCols:', whereCols ) 
        print( 'whereTokenToColMap: ', whereTokenToColMap )
        # Remove tokens already matched
        remainingListOfTokens = []
        for token, pos in list_of_tokens:
            if token not in whereTokenToColMap.keys():
                remainingListOfTokens.append((token, pos))
        return {
            'whereCols': whereCols,
            'whereTokenToColMap': whereTokenToColMap,
            'remainingTokens': remainingListOfTokens 
        }

    # Internal helper function, dont use outside
    def _isfloat( self, token ):
        try:
            float(token)
            return True
        except ValueError:
            return False

    def _isint( self, token ):
        try:
            int(token)
            return True
        except ValueError:
            return False
    
    def _listToLower( self, list_of_tokens ):
        list_of_tokens_tmp = []
        for i in list_of_tokens:
            if str(i) != 'nan' and i != None:
                if isinstance(i, str) or type(i) == 'object':
                    list_of_tokens_tmp.append(i.lower())
                else:
                    list_of_tokens_tmp.append(i)
        return list_of_tokens_tmp

    # Given the list of noun tokens, construct possible where clauses
    def constructWhereCondition( self, list_of_tokens, dbHelper ):
        print('In construct where condition: list_of_tokens: ', list_of_tokens)
        r1 = self.getWhereColumns( list_of_tokens, dbHelper )
        whereCols = r1['whereCols']
        whereTokenToColMap = r1['whereTokenToColMap']
        list_of_tokens = r1[ 'remainingTokens' ]

        print('Remaining List of tokens:', list_of_tokens)
        # For each where column, find corresponding value
        # Assumptions:
        # Doesnt create a where condition if it doesnt return data
        # Only one date value allowed for a where condition e.g. col1 == datevalue1 and col2 == datevalue2
        columnTypeMap = dbHelper.getColumnTypes()
        dateColumns = dbHelper.getDateColumns()
        alnumColumns = dbHelper.getAlphaNumericColumns()
        whereColumnToValueMap = {}
        for whereCol in whereCols:
            whereColValues = []
            whereColType = columnTypeMap.get( whereCol, None )
            print('\n whereCol:', whereCol)
            print('whereColType:', whereColType)
            if( whereColType == 'object' ):  # if token is a string ( alphanumeric or non-alphnumeric)
                if whereCol in dateColumns:  # if column is a date column
                    print('Wherecol is a date')
                    for token, pos in list_of_tokens:
                        if dbHelper.isDateValue( token ): 
                            tokenParsedDate = dbHelper.getParsedDate( token )
                            uniqValues = dbHelper.getUniqueColumnValues( whereCol )
                            print(type(uniqValues[0]))
                            if( tokenParsedDate in uniqValues ):
                                whereColValues.append( tokenParsedDate )
                            else:
                                continue
                        else:
                            continue
                # elif string is a single char ( length of size 1)
                else: # if column is a string column
                    print('Wherecol is a string')
                    uniqValues = dbHelper.getUniqueColumnValues( whereCol )
                    if( len( uniqValues ) != 0 ):
                        uniqValuesLower = self._listToLower( uniqValues )
                        uniqValuesMap = dict(zip( uniqValuesLower, uniqValues ))
                        for token, pos in list_of_tokens:
                            mostSimColumnValue = self.mostSimilar( SimilarityObject(uniqValues), token, False )
                            if mostSimColumnValue != None:
                                print( 'mostSimColumnValue:', mostSimColumnValue )
                                actualWhereValue = uniqValuesMap[ mostSimColumnValue ]
                                print( 'WhereValue:', actualWhereValue )
                                whereColValues.append( actualWhereValue )
                    else:
                        continue
            elif dbHelper.isNumericColumn( whereCol ): # if column is numeric column
                print('Wherecol is a number')
                whereColType = columnTypeMap[ whereCol ]
                for token, pos in list_of_tokens:
                    if pos == 'CD': # Cardinal Digit
                        if whereColType == 'int64':
                            modifiedToken = int(token)
                        if whereColType == 'float64':
                            modifiedToken = float(token)
                        uniqValues = dbHelper.getUniqueColumnValues( whereCol )
                        if modifiedToken in uniqValues:
                            whereColValues.append( token )
                            break
                    else:
                        continue
            else:
                print('Unknown WhereCol:', whereColType)
            whereColValues = list( set( whereColValues ) )
            whereColValues = [ i for i in whereColValues if i ]
            print('whereColValues:', whereColValues)
            whereColumnToValueMap[ whereCol ] = whereColValues
        print( "whereColumnToValueMap: ", whereColumnToValueMap )

        # For each column, find corresponding condition
        whereColumnToConditionMap = {}
        for whereCol in whereCols:
            conditions = []
            colType = columnTypeMap[ whereCol ]
            if( len(whereColumnToValueMap.get( whereCol, [])) > 0 ):
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
        print('Where Clause: ' )
        pp.pprint( whereClause )
        return whereClause

    # Given a list of query tokens, construct the GroupBy clause 
    def constructGroupByClause( self, list_of_tokens ):
        groupByNouns = findGroupByNouns( list_of_tokens ) # returns array of tuples
        groupByCols  = []
        groupByNounToColMap = {}
        for groupByNoun in groupByNouns:
            groupByCol = self.mostSimilar(self.columns, groupByNoun[0])
            if groupByCol is not None:
                groupByNounToColMap[ groupByNoun[0] ] = groupByCol
        print('groupByNounToColMap:', groupByNounToColMap)
        return groupByNounToColMap

    # Given a list of query tokens, construct the Aggregation clause 
    def constructAggregationClause( self, remainingNouns, whereClause  ):
        sqlCommands = set()
        sqlNouns    = set()
        whereTokenToColMap = whereClause[ 'whereTokenToColMap' ]
        aggregationCommandToColumnMap = {}
        prevAggCommand = None
        for noun, pos in remainingNouns:
            aggCommand = self.mostSimilar( self.SQLCommands, noun, True, 2 )
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
        print('nouns without sw: ', nouns_without_sw)

        # Find group by column
        print('\n\nConstructing Group By clause...')
        groupByNounToColMap = self.constructGroupByClause( all_tokens )
        groupByNouns = list(groupByNounToColMap.keys())
        groupByCols = list(groupByNounToColMap.values())
        print("\nGroupByNouns: ", groupByNouns)
        print("\nGroupByCols: ", groupByCols)

        # Remaining nouns after removing repititions and groupByNoun 
        # Using a loop to preserve order
        print('\n\nComputing Remaining nouns (ordered)...')
        remainingNouns = []
        for noun in nouns_without_sw:
            if not (noun in remainingNouns or noun[0] in groupByNouns):
                remainingNouns.append( noun )
        nouns = remainingNouns
        print('Remaining Nouns:', remainingNouns)

        # Find where condition  
        print('\n\nConstructing WHERE clause...')
        whereClause = self.constructWhereCondition( remainingNouns, dbHelper )

        # Construct aggregation clause by associating columns with aggregation functions  
        print('\n\nConstructing Aggregation columns clause...')
        print('\nRemaining Nouns:', remainingNouns)
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
            'selectColumns'                 : selectColumns, # all cols, except agg column
            'aggregationColumns'            : list(aggClause[ 'aggregationCommandToColumnMap' ].keys()),
            'aggregationCommandToColumnMap' : aggClause[ 'aggregationCommandToColumnMap' ],
            'datasetName'                   : 'data',
            'whereColumnNames'              : whereClause[ 'whereColumns' ],
            'whereColumnNameToValueMap'     : whereClause[ 'whereColumnToValueMap' ],
            'whereColumnNameToConditionMap' : whereClause[ 'whereColumnToConditionMap' ],
            'groupbyColumns'                : groupByCols,
            'orderbyColumns'                : [],
            'orderbyColumnToAscDescMap': {}
        }

        print('\n\nsqlObject: ')
        pp.pprint( sqlObj )
        smObj = sm.SQLModule( 
            sqlObj[ 'selectColumns' ], 
            sqlObj[ 'aggregationColumns' ], 
            sqlObj[ 'aggregationCommandToColumnMap' ],
            sqlObj[ 'datasetName' ], 
            sqlObj[ 'whereColumnNames' ], 
            sqlObj[ 'whereColumnNameToValueMap' ],
            sqlObj[ 'whereColumnNameToConditionMap' ], 
            sqlObj[ 'groupbyColumns' ], 
            sqlObj[ 'orderbyColumns' ],
            sqlObj[ 'orderbyColumnToAscDescMap' ] )
        sqlCommand = smObj.formSQLCommand( dbHelper )
        print('sqlCommand:', sqlCommand)
        return sqlCommand
        
if __name__ == "__main__":
    dfName      = 'data'
    df = readDf("table.csv", delimiter = "|")
    # df = readDf("data\dist_pop.txt", delimiter = "|")
    dbHelper    = dh.dbHelper(df)
    columns = dbHelper.getColumnNames()
    print('3')
    ob = SimilarityModule(columns, dfName)
    # inputString = 'give me the total receipts by affiliation'
    # inputString = 'give me the median of receipts by affiliation'
    # inputString = 'give me the average of receipts by affiliation'
    # inputString = 'give me the maximum of receipts by affiliation'
    # inputString = 'give me the minimum of receipts by year'
    # inputString = 'find candidates having candidate id H0AK00055'
    # inputString = 'find candidates in election year 2016'
    # inputString = 'give me the total receipts in election year 2016 by affiliation' # doesnt work because receipts also has a value of 2016
    # inputString = 'give me the number of candidates in election year 2016 by affiliation'
    # inputString = 'find number of candidates and total receipts by affiliation'
    # inputString = 'find number of candidates and total receipts by affiliation and year'
    inputString   = 'find the total population by state'
    sqlCommand    = ob.SQLSuggestion(inputString, dbHelper)
    outGen        = outGen.outputGen( df, sqlCommand )
    result        = outGen.getOutputDf()
    print(result.head(10))

