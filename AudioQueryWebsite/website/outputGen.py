from pandasql import sqldf
from pandasql import load_meat
from website.similarityHelper import *

# pysqldf = lambda q: sqldf(q, globals())

# Class takes arguments sqlObj and sqlCommand and returns a result dataframe 
class outputGen( object ):

    def __init__( self, df, sqlCommand ):
        self.df = df
        self.sqlCommand = sqlCommand

    def getOutputDf( self ):
        data = self.df
        outDf = sqldf(self.sqlCommand, locals())
        return outDf

if __name__ == "__main__":
    df = readDf( 'data\cand_summary.txt', delimiter = '|' )
    # outGen = outputGen( df, 'select * from data d where election_cycle_yr = 2016 LIMIT 10' )
    outGen = outputGen( df, 'select pty_affiliation, election_cycle_yr, count( other_pol_cmte_contrib ), sum( ttl_receipts ) from data group by pty_affiliation, election_cycle_yr' )
    outDf = outGen.getOutputDf()
    print(outDf)