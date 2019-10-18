class SQLModule(object):
    '''
    Instantiates a SQLModule object
    input:
    filename -string for filename of dictionary
    returns:
    SQLModule
    '''
    def __init__(self,filename):
        self.map = None#open the serialized pickled dictionary
    '''
    Forms a SQL command in string format given our system's base SQL
    structure:
    
    'SELECT ' + (id1)Opt(SUM, COUNT...)(id2-[ids])(col_ids) + 'FROM' + [df] + (id3)'GROUP BY' + (id4)col_id'
    (id5) 'WHERE' + (id6)col_id + (id7)condition + (id8) comparision
    input:
    ids - list of id numbers
    returns:
    string - sql command
    '''
    def formSQLCommand(self, ids):
        pass
    
