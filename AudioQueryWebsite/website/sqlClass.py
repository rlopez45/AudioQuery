import pandas as pd
import sqlite3
dbName = 'table.csv'
class sqlClass(object):
    
    def __init__(self, df):
        self.df = df
    def exe(self, query,dbName):
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute(query)
        returnVal = c.fetchall()
        conn.close()
        return returnVal
    def sql2Pandas(self,sqlOutput):
        pass
#pandas.read_sql_query
if __name__ == "__main__":
    df = pd.read_csv(dbName)
    conn = sqli
    s = sqlClass(df)
    
        
    
