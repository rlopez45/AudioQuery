import re
import pandas as pd
from dateutil.parser import parse
import datetime
from similarityHelper import *

class dbHelper():

    def __init__( self, df ):
        df.columns = [i.lower() for i in df.columns]
        self.df = df

    # Get dataframe size 
    def getDfSize( self ):
        return len( self.df )

    def isValidColumn( self, column ):
        return ( column.lower() in self.getColumnNames() )

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
        # try:
        colTypesMap = self.getColumnTypes()
        colType = colTypesMap.get( columnName, None )
        uniqueValues = []
        if( colType == 'float64' or colType == 'int64' or colType == 'object' ):
            uniqueValues = self.df[ columnName ].unique()
        else:
            print( 'Unknown colType!' )
        return uniqueValues

    # Find average token size for column, based on which we can search for column names in the input text
    def getAverageTokenSizeForColumnName( self, delimiters = '_|,\/.?()' ):
        sumOfTokensSize = 0
        columnNames = self.getColumnNames()
        for columnName in columnNames:
            columnNameTokens = re.split(delimiters, columnName.lower())
            columnNameTokens = list(filter(None, columnNameTokens))
            numOfTokens = len( columnNameTokens )
            sumOfTokensSize = sumOfTokensSize + numOfTokens
        return ( sumOfTokensSize / len(columnNames) )

    def getParsedDate( self, token, convertToStr = True ):
        parsedDate = pd.to_datetime(token, infer_datetime_format=True) # <class 'pandas._libs.tslibs.timestamps.Timestamp'>
        format = '%Y-%m-%d %H:%M:%S'
        if convertToStr:
            datetime_str = datetime.datetime.strftime(parsedDate, format)
        else:
            datetime_str = parsedDate
        return parsedDate

    def isDateValue( self, token ):
        try: 
            parse(token, fuzzy=False)
            return True
        except ValueError:
            return False

    # FInd if a column is a date column based on its values
    def isDateColumn( self, column ):
        if self.isValidColumn( column ):
            validValues = self.df[column.lower()][self.df[column.lower()].notna()].unique()
            if len(validValues):
                columnValue = validValues[0]
                try: 
                    parse(columnValue, fuzzy=False)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return False
        
    #  Find all date columns in the dataframe
    def getDateColumns( self ):
        dateColumns = []
        colTypesMap = self.getColumnTypes()
        for column, columnType in colTypesMap.items():
            if columnType == 'object':
                if self.isDateColumn( column ):
                    dateColumns.append( column.lower() )
            elif 'date' in columnType.str.lower():
                dateColumns.append( column.lower() )        
        return dateColumns

    def isAlNumColumn( self, column ):
        if self.isValidColumn( column ):
            validValues = self.df[column.lower()][self.df[column.lower()].notna()].unique()
            if len(validValues):
                columnValue = validValues[0]
                return columnValue.isalnum()
            else:
                return False
        else:
            return False

    def getAlphaNumericColumns( self ):
        alnumColumns = []
        colTypesMap = self.getColumnTypes()
        for column, columnType in colTypesMap.items():
            if columnType == 'object' and self.isAlNumColumn( column.lower() ):
                alnumColumns.append( column.lower() )
        return alnumColumns

    def isNumericColumn( self, column ):
        column = column.lower()
        colTypesMap = self.getColumnTypes()
        colType = colTypesMap.get( column, '' )
        if self.isValidColumn( column ):
            if ( colType == 'float64' or colType == 'int64' ):
                return True
            else:
                return False
        else:
            return False
    
if __name__ == "__main__":
    df = readDf("data\cand_summary.txt", delimiter = "|")
    dbHelper = dbHelper( df )
    print( '\nSize: ', dbHelper.getDfSize() )
    print( '\nColumns: ', dbHelper.getColumnNames() )
    print( '\nCol Types: ', dbHelper.getColumnTypes() )
    u1 = dbHelper.getUniqueColumnValues( 'pty_affiliation' )
    print( '\nUnique Col Values: ', u1 )
    print( '\nAverage Column Token Size: ', dbHelper.getAverageTokenSizeForColumnName() ) 
    dbHelper.isDateColumn('PTY_AFFILIATION')
    print( '\nDate Columns:', dbHelper.getDateColumns())
    # print(parse('H8AK00074', fuzzy = False))
    print( '\nIs Numeric Column PTY_AFFILIATION:', dbHelper.isNumericColumn('PTY_AFFILIATION') )
    print(dbHelper.getParsedDate('2016'))
    # print(dbHelper.getParsedDate('20Jan2016'))

