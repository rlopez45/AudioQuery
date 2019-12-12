import pandas as pd
import os
import pickle
from website.SpeechToTextModule import *
from website.dbHelper import *
from website.SimilarityModule import *
import website.outputGen as oG
from website.VisualizationModule import *
from website.txt2Image import *
dir_path = os.path.dirname(os.path.realpath(__file__))

stateName = 'state.p'
static_website_path =dir_path + "\\static\\website"

class stateClass(object):
    def __init__(self):
        self.csvPath = 'x'
        self.audioQueryPath = 'x'
        self.audioModifyPath = 'x'
    def setCsv(self, path):
        self.csvPath = path
    def setQuery(self, path):
        self.audioQueryPath = path
    def setModify(self, path):
        self.audioModifyPath = path
    def getPath(self):
        return dir_path
    def valid(self):
        return self.csvPath!='x' and self.audioQueryPath!='x'
    def processQuery(self,text ):
        if self.valid():
            try:
                df = pd.read_csv(self.csvPath)
            except:
                df = pd.read_csv(self.csvPath, delimiter = "|")
            dfName      = 'data'
            d = dbHelper(df)
            columns = d.getColumnNames()
            ob = SimilarityModule(columns, dfName)
            sqlCommand = ob.SQLSuggestion(text, d)
            outGen = oG.outputGen( df, sqlCommand )
            result = outGen.getOutputDf()
            print('this is the type')
            print(type(result))
            return result
    
    def getAudioText(self):
        stt = SpeechToTextModule()
        audioFile = self.audioQueryPath
        AUDIO_FILE = stt.loadAudioFile(
            audioFile
        )
        text  = stt.convertSpeechToText( AUDIO_FILE )
        return text
    def getRecs(self, df):
        if self.valid():  
            v = VisualizationModule(df)
            return v.visualization_recommendation()
    
    def getCols(self, df,ctype):
        if self.valid():
            v = VisualizationModule(df)
            v.visualization_recommendation()
            return v.chart_to_columns_recommendation(ctype)
    
    def saveString(self, string, filename,imagefilename):
        print('saving')
        path = dir_path + "\\" +  filename
        file1 = open(path,"w") 
        file1.write(string)
        file1.close()
        image = text_image(path)
        image_path = static_website_path + "\\" + imagefilename
        image.save(image_path)
    def getRecImage(self, df):
        recs = self.getRecs(df)
        s = ''
        keys = recs.keys()
        for key in keys:
            val = recs[key]
            s += str(val) + ": " + "(" + str(val) + ")"
        self.saveString(s, 'rec.txt', 'chartText.jpg')


    def getColumnImage(self, df):
        ctype = None
        pChart_path = dir_path + "\\" + "chartInput.txt"
        with open(pChart_path) as f:
            ctype = f.readline()
        ctype = ctype.strip()
        print(ctype)
        columns = self.getCols(df,ctype)
        print(columns)
        s = ''
        counter = 0
        for col in columns:
            if len(col) == 0:
                continue
            string = "".join(col)
            s += string + " (" + str(counter) + ")"
            counter += 1
        self.saveString(s,'col.txt', 'colText.jpg')
    def printPaths(self):
        print(self.csvPath)
        print(self.audioQueryPath)
        print(self.audioModifyPath)

    def setVisualization(self,df):
        ctype = None
        pChart_path = dir_path + "\\" + "chartInput.txt"
        with open(pChart_path) as f:
            ctype = f.readline()
        ctype = ctype.strip()
        print(ctype)
        i_path = dir_path + "\\" + "colInput.txt"
        index = '0'
        with open(i_path) as f:
            index = f.readline()
        index = index.strip()
        index = int(index)
        columns = self.getCols(df,ctype)
        cols= columns[index]
        v = VisualizationModule(df)
        rest = (v, ctype, cols)
        return (v.dataset_to_visualization(cols,ctype),rest)

    def makeModification(self, df):
        plot,rest = self.setVisualization(df)
        vm ,cols,ctype = rest
        s = SpeechToTextModule()
        modifyFile = self.audioModifyPath
        inter = s.getVisualizationOptions(modifyFile)
        vm.visualization_modification(inter[0], inter[1])
        path = static_website_path + "\\" + "visualization.jpg"
        vm.plot.savefig(path)
        
    def reset(self):
        self.csvPath = 'x'
        self.audioQueryPath = 'x'
        self.audioModifyPath = 'x'

    def printSelf(self):
        print('what\'s up ')

if __name__ == "__main__":
    s = stateClass()
    pickle.dump(s, open(stateName, 'wb'))

