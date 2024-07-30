import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import datetime
import os

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def greet():
    """Greet the user based on the time of day."""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am JARVIS. How can I assist you today?")

def take_command():
    """Listen for commands from the user."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

# def main():
#     greet()
#     while True:
#         query = take_command().lower()

#         if 'wikipedia' in query:
#             speak('Searching Wikipedia...')
#             query = query.replace("wikipedia", "")
#             results = wikipedia.summary(query, sentences=2)
#             speak("According to Wikipedia")
#             print(results)
#             speak(results)

#         elif 'open youtube' in query:
#             webbrowser.open("youtube.com")

#         elif 'open google' in query:
#             webbrowser.open("google.com")

#         elif 'play music' in query:
#             music_dir = 'D:\\Music'  # Change this to your music directory
#             songs = os.listdir(music_dir)
#             os.startfile(os.path.join(music_dir, songs[0]))

#         elif 'the time' in query:
#             str_time = datetime.datetime.now().strftime("%H:%M:%S")
#             speak(f"The time is {str_time}")

#         elif 'exit' in query:
#             speak("Goodbye!")
#             break

# if __name__ == "__main__":
#     main()
speak("hello")