#  Find the token associated with a for each token occurence
#  We assume the token associated with for each will occur right after 
def findForEach(list_tokens):
    for i in range(len(list_tokens)-1):
        curr = list_tokens[i][0]
        next = list_tokens[i+1][0]
        if curr == 'for' and next =='each':
            if i+2<len(list_tokens):
                return list_tokens[i-2]
    return None

#  Extract noun token from a list of tokens
#  Token is a tuple of the form ( token string, part of speech )
def getNouns(list_tokens):
    nouns = []
    for token in list_tokens:
        string, pos = token
        if 'n' in pos.lower():
            nouns.append(token)
    return nouns

#  Strip lines from a file of leading and trailing whitespaces
def parseSQL(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines


if __name__ == "__main__":
    filename = "SupportedSQLCommands.txt"
    result = parseSQL(filename)
    
    
