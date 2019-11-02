# AudioQuery

## Installation Instructions
### SpeechToTextModule
The speech to text module require installing the following python packages:
1. SpeechRecognition (https://pypi.org/project/SpeechRecognition/?fbclid=IwAR1AAtRofCY66RIU5uBqf8Pyegi6bUhDIs9kaJveM6jPgRMo7gb7cvIk63k)
2. Visual Studio CPP Build Tools v14.0 (https://visualstudio.microsoft.com/visual-cpp-build-tools/)
3. PyAudio: This installation dependa on (2) above. To install PyAudio on Windows:
   Go to https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio and download the appropriate PyAudio version for 
   your Python version and OS version (32bit vs 64 bit)
   Then follow the steps here: https://www.youtube.com/watch?v=CeFWBzzcj8o
   We are going with the above hack because pip install PyAudio doesnt work. We also tried installing PyAudio using anaconda 
   and using that, but that dint work either.

