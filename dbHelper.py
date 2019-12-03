import re
import pandas as pd

class dbHelper():

    def __init__( self, df ):
        df.columns = [i.lower() for i in df.columns]
        self.df = df

    # Get dataframe size 
    def getDfSize( self ):
        return len( self.df )

    # Returns the columnnames for the dataset
    def getColumnNames( self ):
        columns = [i.lower() for i in self.df.columns]
        return columns

    # Returns the column name to column type map
    def getColumnTypes( self ):
        colTypesMap = self.df.dtypes.to_dict()
        keys = [i.lower() for i in colTypesMap.keys()]
        colTypesMap = dict(zip( keys, colTypesMap.values() ))
        return colTypesMap

    # Given a column name, get the unique values  
    def getUniqueColumnValues( self, columnName ):
        print(columnName)
        # try:
        colTypesMap = self.getColumnTypes()
        print( colTypesMap )
        colType = colTypesMap.get( columnName, None )
        uniqueValues = []
        print('ColType:', colType)
        if( colType == None ):
            print( 'colType is None' )
        elif( colType == 'float64' ):
            print( 'colType is float64' )
        elif( colType == 'int64' or colType == 'object' ):
            uniqueValues = self.df[ columnName ].unique()
        else:
            print( 'Unknown colType!' )
        return uniqueValues
        # except:
        #     print( 'Exception:' )

    # Find average token size for column, based on which we can search for column names in the input text
    def getAverageTokenSizeForColumnName( self, delimiters = '_|,\/.?()' ):
        sumOfTokensSize = 0
        columnNames = self.getColumnNames()
        for columnName in columnNames:
            columnNameTokens = re.split(delimiters, columnName.lower())
            columnNameTokens = list(filter(None, columnNameTokens))
            print(columnNameTokens)
            numOfTokens = len( columnNameTokens )
            sumOfTokensSize = sumOfTokensSize + numOfTokens
        return ( sumOfTokensSize / len(columnNames) )

if __name__ == "__main__":
    print('dbHelper')
    df = pd.read_csv("data\cand_summary.txt", delimiter = "|")
    dbHelper = dbHelper( df )
    print( '\nSize: ', dbHelper.getDfSize() )
    print( '\nColumns: ', dbHelper.getColumnNames() )
    print( '\nCol Types: ', dbHelper.getColumnTypes() )
    u1 = dbHelper.getUniqueColumnValues( 'PTY_AFFILIATION' )
    print( '\nUnique Col Values: ', u1 )
    print( '\nAverage Column Token Size: ', dbHelper.getAverageTokenSizeForColumnName() ) 

