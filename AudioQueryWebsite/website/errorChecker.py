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
		orderbyColumns ):
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
	def checkSQLObjectValidity( self ):
		if( self.aggregationColumns != [] and self.groupbyColumns == [] ):
			print( "Error!" )
		elif( not (len( self.whereColumnNames ) == len( self.whereColumnNameToValueMap.keys() ) == len( self.whereColumnNameToConditionMap.keys() ) )):
			print( "Error!" )
		else:
			print('Success!')


# Error Checker
if __name__ == "__main__":
	sqlObj = {   
		'selectColumns': ['other_pol_cmte_contrib', 'cand_id'], 
		'aggregationColumns': [], 
		'aggregationCommandToColumnMap': {}, 
		'datasetName': 'data', 
		'whereColumnNames': {'other_pol_cmte_contrib', 'cand_id'}, 
		'whereColumnNameToValueMap': {'other_pol_cmte_contrib': [], 'cand_id': ['h0ak00055']}, 
		'whereColumnNameToConditionMap': {'other_pol_cmte_contrib': [], 'cand_id': ['=']}, 
		'groupbyColumns': [], 
		'orderbyColumns': [], 
		'orderbyColumnToAscDescMap': {}}
	ec = ErrorCheckerModule( sqlObj[ 'selectColumns' ], 
	sqlObj[ 'aggregationColumns' ], sqlObj[ 'aggregationCommandToColumnMap' ],
	sqlObj[ 'datasetName' ], sqlObj[ 'whereColumnNames' ], sqlObj[ 'whereColumnNameToValueMap' ],
	sqlObj[ 'whereColumnNameToConditionMap' ], sqlObj[ 'groupbyColumns' ], sqlObj[ 'orderbyColumns' ])
	ec.checkSQLObjectValidity()


