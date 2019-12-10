# AudioQuery

## Installation Instructions
### SpeechToTextModule
The speech to text module require installing the following python packages:
1. SpeechRecognition (https://pypi.org/project/SpeechRecognition/?fbclid=IwAR1AAtRofCY66RIU5uBqf8Pyegi6bUhDIs9kaJveM6jPgRMo7gb7cvIk63k)
2. Visual Studio CPP Build Tools v14.0 (https://visualstudio.microsoft.com/visual-cpp-build-tools/). This will take up 5-10GB of         space on Windows
3. PyAudio: This installation depends on (2) above. To install PyAudio on Windows:
   Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and download the appropriate PyAudio version for 
   your Python version and OS version (32bit vs 64 bit). For eg, for Python 3.7 and Win 64, this will be of help: PyAudio-0.2.11-cp37-cp37m-win_amd64.whl.
   
   Then follow the steps here: https://www.youtube.com/watch?v=CeFWBzzcj8o
   We are going with the above hack because pip install PyAudio doesnt work. We also tried installing PyAudio using anaconda 
   and using that, but that dint work either.

SpeechToText examples: https://github.com/Uberi/speech_recognition/blob/master/examples/microphone_recognition.py

### Similarity Module
1. Install NLTK
2. Download the 'stopwords', 'wordnet', 'punkt' packages from nltk.
    e.g. nltk.download('stopwords')
3. nltk.download('punkt') is needed for nltk.word_tokenize()
4. nltk.download('averaged_perceptron_tagger') also needed
5. nltk.download('maxent_ne_chunker')
6. nltk.download('words')
7. nltk.download('tree') 
8. nltk.download('treebank')


## Examples
### Unstructured input examples:
1. give me the total receipts for each affiliation
2. give me candidate counts by candidate id



