
import speech_recognition as sr
import pyttsx3
import json

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def load_keywords():
    with open("keywords.json", "r") as f:
        return json.load(f)

def voice_to_code():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    keywords = load_keywords()

    speak("Listening for voice command.")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        for key, code in keywords.items():
            if key in command:
                speak(f"Running command: {key}")
                print(code)
                exec(code)
                return
        speak("Command not recognized.")
    except sr.UnknownValueError:
        speak("Sorry, I did not understand.")
    except Exception as e:
        speak(f"Error: {str(e)}")
