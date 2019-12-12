from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import pickle
import os 
import sys 
import subprocess
import pandas as pd
from pandas.plotting import table
import matplotlib.pyplot as plt 
import imgkit
import sys
import pdfkit
import shutil
from website.StateClass import stateClass
import random

wkhtmltopdf_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
wkhtmltoimage_path = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltoimage.exe"

if wkhtmltopdf_path not in sys.path:
    sys.path.append(wkhtmltopdf_path)


tableName = 'table.csv'
stateFile = 'state.p'

dir_path = os.path.dirname(os.path.realpath(__file__))
print(dir_path)
end = len("website")+1
manage_dir_path = dir_path[:-end]
print(manage_dir_path)
static_website_path =dir_path + "\\static\\website"
print(static_website_path)


def openState():
    files = os.listdir(dir_path)
    state = None
    b = stateFile in files
    path = dir_path + '\\' + stateFile
    if stateFile in files:
        state = pickle.load(open(path, 'rb'))
    if state == None:
        state = stateClass()
        return state

    return state

def saveUploaded(file,name):
    files = os.listdir(dir_path)
    fs = FileSystemStorage(location = dir_path)
    if name in files:
        os.remove(dir_path+"\\"+name)
    fs.save(name,file)

def moveFile(file_name):
    curr_file_path = manage_dir_path+ "\\" + file_name
    new_file_path = static_website_path + "\\" + file_name
    shutil.move(curr_file_path, new_file_path)



def setTablePreview(df):
    df = df.head(10)
    html = df.to_html()
    html_file = open("htmlDf.html", "w+")
    html_file.write(html)
    html_file.close()
    img_file_name = "tablePreview.jpg"
    imgkitoptions = {"format": "jpg"}
    configuration =  imgkit.config(
                    wkhtmltoimage = 
                    wkhtmltoimage_path)
    imgkit.from_file("htmlDf.html",img_file_name,
                    options = imgkitoptions,
                    config = configuration)
    moveFile(img_file_name)

def processUpload(state, file,name):
    saveUploaded(file,name)
    table_path = dir_path + "\\" + tableName
    try:
        df = pd.read_csv(table_path)
    except:
        df = pd.read_csv(table_path, delimiter = "|")
    setTablePreview(df)

def saveState(state):
    pickle.dump(state, open(dir_path + "\\" +"state.p", "wb"))

def delFile(name):
    files = os.listdir(dir_path)
    if name in files:
        os.remove(dir_path+"\\"+name)

def delFiles():
    delFile(tableName)
    delFile('audioQuery.wav')
    delFile('modifyData.wav')

def processPost(request):
    files = request.FILES
    state = openState()
    if 'csvData' in files:
        uploaded_file = request.FILES['csvData']
        processUpload(state,uploaded_file,tableName)
        csvPath = dir_path + "\\" + tableName
        state.setCsv(csvPath)
    elif 'audioData' in files:
        uploaded_file = request.FILES['audioData']
        saveUploaded(uploaded_file,'audioQuery.wav')
        audioPath = dir_path + "\\" + 'audioQuery.wav'
        state.setQuery(audioPath)
        
    elif 'modifyData' in files:
        uploaded_file = request.FILES['modifyData']
        saveUploaded(uploaded_file,'modifyQuery.wav')
        modifyPath = dir_path + "\\" + 'modifyQuery.wav'
        state.setModify(modifyPath)
        df = None
        result_path = dir_path + "\\" + "result.csv"
        try:
            df = pd.read_csv(result_path)
        except:
            df = pd.read_csv(result_path,delimiter = "|")
        state.makeModification(df)
    elif 'chartInput' in files:
        uploaded_file = request.FILES['chartInput']
        saveUploaded(uploaded_file, 'chartInput.txt')
        result_path = dir_path + "\\" + "result.csv"
        try:
            df = pd.read_csv(result_path)
        except:
            df = pd.read_csv(result_path,delimiter = "|")
        state.getColumnImage(df)
    elif 'colInput' in files:
        uploaded_file = request.FILES['colInput']
        saveUploaded(uploaded_file, 'colInput.txt')
        result_path = dir_path + "\\" + "result.csv"
        df = None
        try:
            df = pd.read_csv(result_path)
        except:
            df = pd.read_csv(result_path,delimiter = "|")
        plot,viz = state.setVisualization(df)
        vis_path = static_website_path + "\\" + "visualization.jpg"
        plot.savefig(vis_path)
    else:
        text = state.getAudioText()
        df = state.processQuery(text)
        result_path = dir_path + "\\" + "result.csv"
        df.to_csv(result_path)
        print('making visualization')
        state.getRecImage(df)
        #state.reset()
    saveState(state)
def index(request):
    if request.method == 'POST':
        processPost(request)
    return render(request, 'website/htmlTemplate.html')
