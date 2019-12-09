import speech_recognition as sr 
import time
from os import path

class SpeechToTextModule():
    
    # Converts an audio input into text using the Google Speech to Text API
    # Input:
    # Audio as spoken into the microphone
    # Output:
    # The text (converted from audio)
    def __init__( self ):
        print('\nInitializing Speech Recognizer...')
        self.r = sr.Recognizer()
        print('Speech Recognizer initialized!')

    # Listens to the first phrase and extracts it into audio data
    # audioInput: .wav file, uses microphone input if audio file is not given
    def convertSpeechToText( self, audioFile = None):
        if audioFile:
            audioSource = sr.AudioFile(audioFile)
        else:
            audioSource = sr.Microphone()

        with audioSource as source:
            audio = self.r.listen(source)
            print("Time Over, Thanks")
        try:
            text = self.r.recognize_google(audio)
            print("Converted Text: ", text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # given an audio file location, loads it
    def loadAudioFile( self, audioFileLocation ):
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), audioFileLocation )
        print('Audio File Absolute Location: ', AUDIO_FILE)
        return AUDIO_FILE

if __name__ == "__main__":
    print('\nSay Something, Microphone is recording...')
    stt   = SpeechToTextModule()
    AUDIO_FILE = stt.loadAudioFile( "audio\Sample_Audio_1.wav" )
    start = time.time()
    text  = stt.convertSpeechToText( AUDIO_FILE )
    end   = time.time() 
    print("Time Taken(s): ", end-start)