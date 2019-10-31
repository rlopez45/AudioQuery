import sqlite3
import pandas
class DataModule(object):
    '''
    Instantiates a data module object
    input:
    data- pandas dataframe
    returns:
    data module object
    '''
    def __init__(self, filename):
        self.connection = sqlite3.connect(filename)
        self.df = pd.read_csv(filename)
    '''
    Executes a sql command given as a string
    input:
    stringSQL- command in string format
    returns:
    result - resultant dataframe
    '''
    def exeSQL(self, stringSQL):
        result = crsr.execute(stringSQL)
        return result

    '''
    Creates a dictionary of data schema titles to new id numbers
    input:
    self
    returns:
    dictionary
    '''
    def createIds(self):
        return self.df.columns.copy()
