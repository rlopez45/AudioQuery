class DataModule(object):
    '''
    Instantiates a data module object
    input:
    data- pandas dataframe
    returns:
    data module object
    '''
    def __init__(self, data):
        self.data = data
    '''
    Executes a sql command given as a string
    input:
    stringSQL- command in string format
    returns:
    result - resultant dataframe
    '''
    def exeSQL(self, stringSQL):
        pass

    '''
    Creates a dictionary of data schema titles to new id numbers
    input:
    self
    returns:
    dictionary
    '''
    def createIds(self):
