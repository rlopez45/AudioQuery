import speech_recognition as sr 
class SpeechToTextModule():
    
    def convertSpeechToText( self ):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("SAY SOMETHING: ")
            audio = r.listen(source)
            print("TIME OVER THANKS")
        try:
            text = r.recognize_google(audio)
            print("TEXT: ", text)
            return text
        except Exception as ex:
            print (ex)

if __name__ == "__main__":
    # start = time.time()
    stt  = SpeechToTextModule()
    text = stt.convertSpeechToText()
    # end = time.time()
    # print("Time Taken: ", start-end)
    print("End")