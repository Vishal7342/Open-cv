import pyttsx3
import datetime
import requests
import webbrowser
import os
import pywhatkit
import random
import pyjokes
import pyautogui
import speech_recognition as sr
import wikipedia
import time
import warnings
import tkinter as tk
from transformers import pipeline
from textblob import TextBlob
import json
import openai  # For advanced NLP features

# Suppress warnings
warnings.simplefilter('ignore')

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
from googletrans import Translator
# OpenAI API Key
openai.api_key = 'YOUR_OPENAI_API_KEY'

def speak(audio):
    print(f"Speaking: {audio}")  # Debug statement
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning Sir!")
    elif hour < 18:
        speak("Good Afternoon Sir!")
    else:
        speak("Good Evening Sir!")
    speak("Jarvis Here, an AI Language Model! How may I help you?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        audio = r.listen(source, timeout=5)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except sr.UnknownValueError:
        print("Sorry, I did not understand the audio.")
        speak("Sorry, I did not understand the audio.")
        return "None"
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        speak("Sorry, there was an issue with the speech recognition service.")
        return "None"
    return query.lower()

def advanced_nlp(query):
    # Use OpenAI for advanced NLP tasks
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=query,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def run_alpha():
    query = takeCommand()
    if query == "none":
        return

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
        translator = Translator()
        try:
            translation = translator.translate(text_to_translate, dest=target_language)
            speak(f"Here is the translation: {translation.text}")
        except Exception as e:
            speak("Sorry, I couldn't perform the translation.")
            print(f"Translation error: {e}")

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
        self.label = tk.Label(root, text="Welcome to Jarvis Assistant", padx=20, pady=20)
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
