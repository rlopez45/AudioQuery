class ErrorCheckerModule(object):

	# Initialize the error checker module
    def __init__(self, 
      	selectColumns, 
        aggregationColumns, 
        aggregationCommandToColumnMap,	# e.g. { 'SUM': [ 'ttl_receipts', 'donation_amt' ] }
        datasetName,
        whereColumnNames,
        whereColumnNameToValueMap,
        whereColumnNameToConditionMap,
        groupbyColumns,
        orderbyColumns
	):
        self.selectColumns 				   = selectColumns
        self.aggregationColumns 		   = aggregationColumns
        self.aggregationCommandToColumnMap = aggregationCommandToColumnMap 
        self.datasetName 				   = datasetName
        self.whereColumnNames 			   = whereColumnNames
        self.whereColumnNameToValueMap     = whereColumnNameToValueMap
        self.whereColumnNameToConditionMap = whereColumnNameToConditionMap
        self.groupbyColumns 			   = groupbyColumns
        self.orderbyColumns 			   = orderbyColumns

	# Check if the SQL features generated are valid ones
    def checkSQLObjectValidity():
        if(( self.aggregationColumns == [] & self.groupbyColumns != [] ) or
           ( self.aggregationColumns != [] & self.groupbyColumns == [] )):
            print( "Error!" )
        if( not (len( self.whereColumnNames ) ==
              len( self.whereColumnNameToValueMap.keys() ) == 
              len( self.whereColumnNameToConditionMap.keys() ) )):
                print( "Error!" )
        # To Do: Other checks to be added
