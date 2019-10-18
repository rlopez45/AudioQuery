class SimilarityModule(object):
    '''
    Instantiates a SimilarityModule 
    input:
    dataObj - dataObject that contains pandas df and parsed audio data
    returns:
    SM object
    '''
    def __init__(self,dataObj):
        self.dataObj = dataObj
        self.mlModel = None
    '''
    Gives a similarity score for a string compared to a body of strings
    input:
    string - similarity score to be computed for this string
    d - dictionary whose keys are the body of strings that will compared to string
    returns:
    float - [0, 1]
    '''
    def similarity(self,d, string):
        pass
    '''
    Selects the SQL Command that is most similar to a given string
    input:
    string - user provided audio
    returns:
    ids - list of ids - id maps to a SQL Command
    '''
    def SQLSuggestions(self,string):
        pass
    '''
    Determines whether the user's input will require a dataBase query or not
    input:
    string - audio input of user
    returns:
    True - if needs SQL
    False - o.w.
    '''
    def vizOrSQL(self,string):
        pass
    
