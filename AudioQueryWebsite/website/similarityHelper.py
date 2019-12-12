import nltk
from nltk.corpus import stopwords as sWords
from nltk.corpus import wordnet
from nltk.tree import Tree
from nltk import ne_chunk, pos_tag, word_tokenize
import pandas as pd

#  Deprecated: Find the token(s) associated with a groupby token occurence
#  We assume the token associated with a groupby will occur right after it
def findGroupByClause( list_tokens ):
    for i in range(len(list_tokens)-1):
        curr = list_tokens[i][0]
        next = list_tokens[i+1][0]
        if curr == 'for' and next =='each':
            if i+2 < len(list_tokens):
                return list_tokens[i+2]
        if ( ( curr == 'group' or curr == 'grouped' ) and next == 'by' ):
            if i+2 < len(list_tokens):
                return list_tokens[i+2]
        if curr == 'by':
            if i+1 < len(list_tokens):
                return list_tokens[i+1]
    return None

# Get all group by nouns after a groupby token occurence
def findGroupByNouns( list_tokens ):
    start_idx = None
    end_idx = len(list_tokens)  # To Do: enhance end_idx to stop earlier
    for i in range(len(list_tokens)-1):
        curr = list_tokens[i][0]
        next = list_tokens[i+1][0]
        if  ( curr == 'for' and next =='each' ) or ( ( curr == 'group' or curr == 'grouped' ) and next == 'by' ):
            if i+2 < len(list_tokens):
                start_idx = i+2
        elif curr == 'by':
            if i+1 < len(list_tokens):
                start_idx = i+1
    # collect nouns by looping from start_idx to end of string
    groupByNouns = []
    if start_idx is not None:
        groupByNouns = list_tokens[start_idx: end_idx]
        groupByNouns = getNouns( groupByNouns )
    return groupByNouns

# Find a token associated with ordering or sorting
def findOrderedByClause( list_tokens ):
    for i in range(len[list_tokens]-1):
        curr = list_tokens[i][0]
        next = list_tokens[i+1][0]
        if (( curr == 'order' ) or
           ( curr == 'ordered' ) or
           ( curr == 'sort' ) or 
           ( curr == 'sorted' )) and ( next == 'by' or next == 'using' ):
            if i+2 < len(list_tokens):
                return list_tokens[i+2]
    return None

#  Extract noun token from a list of tokens
#  Token is a tuple of the form ( token string, part of speech )
def getNouns(list_tokens):
    print('Input list: ', list_tokens)
    nouns = []
    for token, pos in list_tokens:
        # including nouns and adjectives. e.g. total is tagged an adjective sometimes
        if 'n' in pos.lower() or 'j' in pos.lower() or pos == 'CD':
            nouns.append((token, pos))
    return nouns

def getNamedEntities( text ):
    sent = pos_tag(word_tokenize(text))
    ne = nltk.ne_chunk(sent)
    prev = None
    continuous_chunk = []
    current_chunk = []
    for i in ne:
        if type(i) == nltk.tree.Tree: # named entity
            print('NE: ', i, '; NE Type: ', i.label())
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        # elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    print('\nContinuous Chunks:', continuous_chunk)

#  Strip lines from a file of leading and trailing whitespaces
def parseSQL( filename ):
    with open(filename) as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    return lines

# Given a dataframe and a delimiter read the dataframe with date parsing
def readDf( dfLocation, delimiter ):
    date_parser = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    df = pd.read_csv(dfLocation, delimiter = delimiter, parse_dates = True, date_parser = date_parser)
    return df

if __name__ == "__main__":
    # filename = "SupportedSQLCommands.txt"
    # result = parseSQL(filename)
    getNamedEntities('give me the number of receipts in January')


