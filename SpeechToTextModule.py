import speech_recognition as sr 
import time

class SpeechToTextModule():
    '''
    Converts an audio input into text using the Google Speech to Text API
    input:
    Audio as spoken into the microphone
    returns:
    The text (converted from audio)
    '''   
    def convertSpeechToText( self ):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("SAY SOMETHING: ")
            # listen for the first phrase and extract it into audio data
            audio = r.listen(source)
            print("TIME OVER THANKS")
        try:
            text = r.recognize_google(audio)
            print("TEXT: ", text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    start = time.time()
    stt   = SpeechToTextModule()
    text  = stt.convertSpeechToText()
    end   = time.time() 
    print("Time Taken(s): ", end-start)