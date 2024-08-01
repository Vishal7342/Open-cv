import tkinter as tk
import webbrowser
import datetime
import os
import pywhatkit
import pyautogui
import requests
import pyjokes
import wikipedia
import random
import time
from transformers import pipeline
from deep_translator import GoogleTranslator
import speech_recognition as sr
from textblob import TextBlob

# Define the takeCommand function
def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return "none"
        except sr.RequestError:
            print("Sorry, I'm having trouble connecting to the service.")
            return "none"

# Define the speak function
def speak(text):
    print(text)  # For simplicity, just print the text

# Define the advanced_nlp function
def advanced_nlp(query):
    # Simple NLP processing example
    if 'weather' in query:
        return "I can help with weather updates, but this feature is not yet implemented."
    elif 'news' in query:
        return "I can provide news updates, but this feature is not yet implemented."
    return "This is a placeholder for advanced NLP responses."

# Emotion detection function
def detect_emotion(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "positive"
    elif sentiment < 0:
        return "negative"
    else:
        return "neutral"

# Context management class
class Context:
    def __init__(self):
        self.last_command = ""

    def update(self, command):
        self.last_command = command

    def get_last_command(self):
        return self.last_command

# Initialize context
context = Context()

def run_alpha():
    query = takeCommand()
    if query == "none":
        return

    context.update(query)

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results for that query. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any results.")

    elif 'open youtube' in query:
        speak('Opening YouTube...')
        webbrowser.open("https://www.youtube.com")

    elif 'open google' in query:
        speak('Opening Google...')
        webbrowser.open("https://www.google.com")

    elif 'open github' in query:
        speak('Opening GitHub...')
        webbrowser.open("https://www.github.com")

    elif 'open discord' in query:
        speak('Opening Discord...')
        webbrowser.open("https://discord.com")

    elif 'search on google' in query:
        speak("What would you like to search on Google?")
        search_query = takeCommand().strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

    elif 'open gmail' in query:
        speak("Opening Gmail...")
        webbrowser.open("https://mail.google.com")

    elif 'play tech burner' in query:
        speak("Playing Tech Burner...")
        webbrowser.open("https://www.youtube.com/@TechBurner")

    elif 'play kaushik shresth' in query:
        speak("Playing Kaushik Shresth...")
        webbrowser.open("https://www.youtube.com/@Kaushikshresth")

    elif 'play my favourite videos' in query:
        speak("Playing your favourite videos...")
        webbrowser.open("https://www.youtube.com/@RAAAZofficial")

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif 'open notepad' in query:
        speak('Opening Notepad...')
        nPath = "C:\\Program Files\\Notepad++\\notepad++.exe"
        if os.path.exists(nPath):
            os.startfile(nPath)
        else:
            speak("Notepad++ is not installed in the default path.")

    elif 'open command prompt' in query:
        speak('Opening Command Prompt...')
        os.system('start cmd')

    elif 'send message' in query:
        speak('Sending message...')
        pywhatkit.sendwhatmsg('number here', 'message here', "time here")

    elif 'play a song' in query:
        song = query.replace('play a song', '').strip()
        speak(f'Playing {song}')
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

    elif "what's up" in query or 'how are you' in query:
        stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am full of energy', 'I am okay! How are you?']
        ans_q = random.choice(stMsgs)
        speak(ans_q)
        ans_take_from_user_how_are_you = takeCommand().lower()
        if 'fine' in ans_take_from_user_how_are_you or 'happy' in ans_take_from_user_how_are_you or 'okay' in ans_take_from_user_how_are_you:
            speak('Okay...')
        elif 'not' in ans_take_from_user_how_are_you or 'sad' in ans_take_from_user_how_are_you or 'upset' in ans_take_from_user_how_are_you:
            speak('Oh sorry...')

    elif 'made you' in query or 'created you' in query or 'developed you' in query:
        ans_m = "For your information, Mr. Arinjoy Acharya created me. I give a lot of thanks to him."
        print(ans_m)
        speak(ans_m)

    elif "hello" in query or "hello jarvis" in query:
        hel = "Hello Sir! How may I help you?"
        print(hel)
        speak(hel)

    elif "your name" in query:
        na_me = "Thanks for asking my name. My name is Jarvis."
        print(na_me)
        speak(na_me)

    elif "you feeling" in query:
        speak("Feeling very energetic after meeting with you.")

    elif "shut up" in query:
        speak("Sorry???")
        exit()

    elif "not feeling well" in query:
        speak("WAIT... Take a deep breath, don't worry...")
        webbrowser.open('https://www.google.com/search?q=doctors+near+me')

    elif "i have fever" in query:
        speak("Take Calpol 650 or 500 according to your health and drink lots of water. You will feel better.")

    elif "ip address" in query:
        try:
            ip = requests.get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")
        except requests.RequestException:
            speak("Sorry, I couldn't retrieve your IP address.")

    elif "tell me a joke" in query:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "location" in query:
        speak("Let me check...")
        try:
            ipAdd = requests.get('https://api.ipify.org').text
            url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
            geo_requests = requests.get(url)
            geo_data = geo_requests.json()
            city = geo_data['city']
            state = geo_data['state']
            country = geo_data['country']
            speak(f"We are in {city}, {state}, {country}.")
        except Exception as e:
            speak("Sorry, I couldn't find your location.")

    elif "take a screenshot" in query:
        speak("Please tell me the name for the screenshot file.")
        name = takeCommand().strip()
        if name == "none":
            speak("Screenshot name not provided.")
            return
        speak("Taking screenshot...")
        time.sleep(2)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        speak("Screenshot saved!")

    elif "summarize" in query:
        speak("What do you want me to summarize?")
        text_to_summarize = takeCommand()
        summarizer = pipeline("summarization")
        summary = summarizer(text_to_summarize, max_length=150, min_length=30, do_sample=False)
        speak("Here is the summary.")
        print(summary[0]['summary_text'])
        speak(summary[0]['summary_text'])

    elif "translate" in query:
        speak("What text would you like me to translate?")
        text_to_translate = takeCommand()
        speak("Which language should I translate to? (e.g., French, Spanish)")
        target_language = takeCommand().lower()
        # Perform translation using deep_translator
        translation = GoogleTranslator(target_lang=target_language).translate(text_to_translate)
        speak(f"Here is the translation: {translation}")

    else:
        response = advanced_nlp(query)
        speak("Accessing database...")
        print(response)
        speak(response)

# GUI Class Definition
class JarvisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis Assistant")
        self.speak_command = None

        # Set up the GUI components
        self.label = tk.Label(root, text="Welcome to Jarvis Assistant", padx=480, pady=20)
        self.label.pack()

        self.button = tk.Button(root, text="Start", command=self.run_command)
        self.button.pack()
        

    def set_speak_command(self, command):
        self.speak_command = command

    def run_command(self):
        if self.speak_command:
            self.speak_command()

# Create Tkinter root and GUI instance
root = tk.Tk()
gui = JarvisGUI(root)
gui.set_speak_command(run_alpha)

# Start the GUI event loop
root.mainloop()
