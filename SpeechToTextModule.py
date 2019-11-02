import speech_recognition as sr 
class SpeechToTextModule() {

    def __init__( ) {

    }
        
    def convertSpeechToText() {
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("SAY SOMETHING: ");
            audio = r.listen(source);
            print("TIME OVER THANKS");
        try:
            print("TEXT: "+r.recognize_google(audio))
    }

}