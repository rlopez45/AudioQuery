import errorChecker as ec
import dbHelper as dbh
import pandas as pd

class SQLModule(object):

    # Instantiates a SQLModule object
    def __init__(self, 
        selectColumns = [], 
        aggregationColumns = [], 
        aggregationCommandToColumnMap = [],
        datasetName = '',
        whereColumnNames = [],
        whereColumnNameToValueMap = {},
        whereColumnNameToConditionMap = {},
        groupbyColumns = [],
        orderbyColumns = [],
        orderbyColumnToAscDescMap = {}
    ):
        # self.map = None # To Do: open the serialized pickled dictionary
        self.selectColumns = selectColumns
        self.aggregationColumns = aggregationColumns
        self.aggregationCommandToColumnMap = aggregationCommandToColumnMap # e.g. { 'SUM': [ 'ttl_receipts', 'donation_amt' ] }
        self.datasetName = datasetName
        self.whereColumnNames = whereColumnNames
        self.whereColumnNameToValueMap = whereColumnNameToValueMap
        self.whereColumnNameToConditionMap = whereColumnNameToConditionMap
        self.groupbyColumns = groupbyColumns
        self.orderbyColumns = orderbyColumns
        self.orderbyColumnToAscDescMap = orderbyColumnToAscDescMap

    # Internal helper function to construct aggregation command
    # Not to be used standalone
    def _getAggregationClause( self, aggregationCmd, aggregationCol ):
        return aggregationCmd.lower() + '( ' + aggregationCol.lower() + ' )'

    # Forms a SQL command in string format given query parameters
    # Input: Query Parameters i.e. select columns, where columns, conditions etc
    # Output: SQL Query
    def formSQLCommand( self, dbHelper ):
        # Error check the SQL command features, function will throw if there are errors
        # ec.checkSQLObjectValidity()
        # Construct SQL command
        selectPhrase    = self.constructSelectPhrase()
        wherePhrase     = self.constructWherePhrase( dbHelper )
        groupByPhrase   = self.constructGroupByPhrase()
        orderByPhrase   = self.constructOrderByPhrase()
        sqlCommand      = selectPhrase + wherePhrase + groupByPhrase + orderByPhrase
        print( '\n SQL Command: ', sqlCommand )
        return sqlCommand

    def constructSelectPhrase( self ):
        print( '\nself.aggregationColumns: ', self.aggregationColumns )
        print( '\nself.selectColumns: ', self.selectColumns )
        groupbyColumns = [i for i in self.groupbyColumns if i]
        selectPhrase = ''
        if( not self.aggregationColumns ):
            if( not self.selectColumns ): # [] or None
                selectPhrase = ' * '
            else:
                if len( groupbyColumns ) == 0:
                    selectPhrase = ' * '
                else:    
                    selectPhrase = ', '.join( self.selectColumns )
        else:
            # collect aggregation select columns
            aggregationList = []
            for aggregationCol, aggregationCmd in self.aggregationCommandToColumnMap.items():
                aggregationList.append( self._getAggregationClause( aggregationCmd, aggregationCol ) )
            print('aggregationList: ', aggregationList)
            # collect any non-aggregation select columns i.e. exclude aggColumns
            # also exclude a column if it is not in groupby col, not agg col, not where col 
            remainingSelectColumns = list(set( self.selectColumns ) - set( self.aggregationColumns ))
            print('remainingSelectColumns: ', remainingSelectColumns)
            validWhereColumns = [i for i in self.whereColumnNameToValueMap.keys() if len(self.whereColumnNameToValueMap[i])]
            print('validWhereColumns:', validWhereColumns)
            remainingSelectColumns = [i for i in remainingSelectColumns if( i in validWhereColumns or i in groupbyColumns)]
            print('remainingSelectColumns: ', remainingSelectColumns)
            # include group by cols if not already included
            groupByColumnsToSelect = [i for i in groupbyColumns if i not in remainingSelectColumns] 
            print('groupByColumnsToSelect:', groupByColumnsToSelect)
            # if( remainingSelectColumns != [] ):
            aggregationList = remainingSelectColumns + groupByColumnsToSelect + aggregationList 
            selectPhrase = ', '.join( aggregationList )
        selectPhrase = 'select ' + selectPhrase + ' from ' + self.datasetName
        print( 'selectPhrase: ', selectPhrase )
        return selectPhrase

    def constructWherePhrase( self, dbHelper ):
        wherePhrase = ''
        wherePhraseList = []
        colTypesMap = dbHelper.getColumnTypes()
        if( self.whereColumnNames != [] ):
            for colName, colValue in self.whereColumnNameToValueMap.items():
                colCondition = self.whereColumnNameToConditionMap.get( colName, ['='] )
                if not colCondition or not colValue:
                    continue
                if len( colValue ):
                    if( colTypesMap.get( colName, '' ) == 'object' ):  # if colType is string enclose with quotes
                        colValue = ['\'{}\''.format(i) for i in colValue] 
                    colValue = ', '.join( colValue )
                print(colName)
                print(colCondition)
                print(colValue)
                wherePhraseList.append( colName + ' ' + colCondition[0] + ' ' + colValue )
            if wherePhraseList:
                wherePhrase = ' where ' + ' and '.join( wherePhraseList )
        print( 'wherePhrase: ', wherePhrase )
        return wherePhrase

    def constructGroupByPhrase( self ):
        groupByPhrase = ''
        groupbyColumns = [i for i in self.groupbyColumns if i]
        if( groupbyColumns ):
            groupByPhrase = ' group by ' + ', '.join( groupbyColumns )
        print( 'groupByPhrase: ', groupByPhrase )
        return groupByPhrase

    def constructOrderByPhrase( self ):
        orderByPhrase = ''
        if( self.orderbyColumns ):
            orderByPhrase = 'order by ' + ', '.join( self.orderbyColumns ) + ' asc'
        # To do: enhance with asc desc map, etc
        return orderByPhrase

if __name__ == "__main__":
    
    df = pd.read_csv("data\cand_summary.txt", delimiter = "|")
    dbHelper = dbh.dbHelper( df )
    print( '\nSize: ', dbHelper.getDfSize() )
    print( '\nColumns: ', dbHelper.getColumnNames() )
    print( '\nCol Types: ', dbHelper.getColumnTypes() )

    sqlObj = {   
        'selectColumns': ['other_pol_cmte_contrib', 'cand_id'], 
        'aggregationColumns': [], 
        'aggregationCommandToColumnMap': {}, 
        'datasetName': 'data', 
        'whereColumnNames': {'other_pol_cmte_contrib', 'cand_id'}, 
        'whereColumnNameToValueMap': {'other_pol_cmte_contrib': [], 'cand_id': ['h0ak00055']}, 
        'whereColumnNameToConditionMap': {'other_pol_cmte_contrib': [], 'cand_id': ['=']}, 
        'groupbyColumns': None, 
        'orderbyColumns': [], 
        'orderbyColumnToAscDescMap': {}}
    sm = SQLModule( sqlObj[ 'selectColumns' ], sqlObj[ 'aggregationColumns' ], sqlObj[ 'aggregationCommandToColumnMap' ],
                    sqlObj[ 'datasetName' ], sqlObj[ 'whereColumnNames' ], sqlObj[ 'whereColumnNameToValueMap' ],
                    sqlObj[ 'whereColumnNameToConditionMap' ], sqlObj[ 'groupbyColumns' ], sqlObj[ 'orderbyColumns' ],
                    sqlObj[ 'orderbyColumnToAscDescMap' ] )
    sm.formSQLCommand( dbHelper )