import pyttsx3
import datetime
import webbrowser
import os
import random
import pyjokes
import pyautogui
import speech_recognition as sr
import wikipedia
import time
import warnings
import threading
import psutil
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.animation import Animation
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup
import requests
import re
import spacy
from textblob import TextBlob
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Suppress warnings
warnings.simplefilter('ignore')

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Initialize cookie storage
cookies = SimpleCookie()

def speak(audio):
    print(f"Speaking: {audio}")
    engine.say(audio)
    engine.runAndWait()

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
        return "none"
    except sr.RequestError:
        print("Sorry, there was an issue with the speech recognition service.")
        speak("Sorry, there was an issue with the speech recognition service.")
        return "none"
    return query.lower()

def process_text(text):
    """Process text to extract intent, entities, and perform sentiment analysis."""
    # NLP Pipeline
    doc = nlp(text)
    
    # Extract Entities
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Extract Sentiment
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    
    # Tokenization and Lemmatization
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
    
    return tokens, entities, sentiment

def search_wikipedia(query):
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

def open_youtube():
    speak('Opening YouTube...')
    webbrowser.open("https://www.youtube.com")

def open_google():
    speak('Opening Google...')
    webbrowser.open("https://www.google.com")

def open_github():
    speak('Opening GitHub...')
    webbrowser.open("https://www.github.com")

def open_discord():
    speak('Opening Discord...')
    webbrowser.open("https://discord.com")

def search_on_google():
    speak("What would you like to search on Google?")
    search_query = takeCommand().strip()
    if search_query == "none":
        return
    webbrowser.open(f"https://www.google.com/search?q={search_query}")

def open_gmail():
    speak("Opening Gmail...")
    webbrowser.open("https://mail.google.com")

def play_tech_burner():
    speak("Playing Tech Burner...")
    webbrowser.open("https://www.youtube.com/@TechBurner")

def play_kaushik_shresth():
    speak("Playing Kaushik Shresth...")
    webbrowser.open("https://www.youtube.com/@Kaushikshresth")

def play_my_favourite_videos():
    speak("Playing your favourite videos...")
    webbrowser.open("https://www.youtube.com/@RAAAZofficial")

def tell_time():
    strTime = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The time is {strTime}")

def open_notepad():
    speak('Opening Notepad...')
    nPath = "C:\\Program Files\\Notepad++\\notepad++.exe"
    if os.path.exists(nPath):
        os.startfile(nPath)
    else:
        speak("Notepad++ is not installed in the default path.")

def open_command_prompt():
    speak('Opening Command Prompt...')
    os.system('start cmd')

def send_message():
    speak('Sending message...')
    pywhatkit.sendwhatmsg('number here', 'message here', "time here")

def play_song(query):
    song = query.replace('play a song', '').strip()
    speak(f'Playing {song}')
    webbrowser.open(f"https://www.youtube.com/results?search_query={song}")

def whats_up():
    stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am full of energy', 'I am okay! How are you?']
    ans_q = random.choice(stMsgs)
    speak(ans_q)
    ans_take_from_user_how_are_you = takeCommand().lower()
    if 'fine' in ans_take_from_user_how_are_you or 'happy' in ans_take_from_user_how_are_you or 'okay' in ans_take_from_user_how_are_you:
        speak('Okay...')
    elif 'not' in ans_take_from_user_how_are_you or 'sad' in ans_take_from_user_how_are_you or 'upset' in ans_take_from_user_how_are_you:
        speak('Oh sorry...')

def who_made_you():
    ans_m = "For your information, Mr. Arinjoy Acharya created me. I give a lot of thanks to him."
    print(ans_m)
    speak(ans_m)

def say_hello():
    hel = "Hello Sir! How may I help you?"
    print(hel)
    speak(hel)

def your_name():
    na_me = "Thanks for asking my name. My name is Jarvis."
    print(na_me)
    speak(na_me)

def how_feeling():
    speak("Feeling very energetic after meeting with you.")

def shut_up():
    speak("Sorry???")
    App.get_running_app().stop()
    return

def not_feeling_well():
    speak("WAIT... Take a deep breath, don't worry...")
    webbrowser.open('https://www.google.com/search?q=doctors+near+me')

def have_fever():
    speak("Take Calpol 650 or 500 according to your health and drink lots of water. You will feel better.")

def ip_address():
    speak("Sorry, this feature requires an internet connection.")

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def get_location():
    speak("Sorry, this feature requires an internet connection.")

def take_screenshot():
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

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    speak(f"CPU usage is at {cpu_usage} percent. Memory usage is at {memory.percent} percent.")

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(ISimpleAudioVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(ISimpleAudioVolume)
    volume.SetMasterVolume(level / 100.0, None)
    speak(f"Volume set to {level} percent.")

def search_files(query):
    speak("Searching for files...")
    query = query.replace("search for files", "").strip()
    result = []
    for root, dirs, files in os.walk("C:\\"):
        for file in files:
            if query in file:
                result.append(os.path.join(root, file))
    if result:
        speak(f"Found {len(result)} files matching your query.")
        for file in result:
            print(file)
    else:
        speak("No files found matching your query.")

def store_cookie(key, value):
    cookies[key] = value
    speak(f"Cookie with key {key} and value {value} stored.")

def retrieve_cookie(key):
    value = cookies.get(key, "Key not found")
    speak(f"Value for {key} is {value}")

def scrape_data(url):
    speak(f"Scraping data from {url}...")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.get_text()
        speak("Data scraped successfully.")
        print(data)
    except Exception as e:
        speak("Sorry, I couldn't scrape the data.")
        print(e)

def run_alpha():
    query = takeCommand()
    if query == "none":
        return

    tokens, entities, sentiment = process_text(query)
    
    # Implement command handling logic
    if 'wikipedia' in tokens:
        search_wikipedia(query)
    elif 'open' in tokens:
        if 'youtube' in tokens:
            open_youtube()
        elif 'google' in tokens:
            open_google()
        elif 'github' in tokens:
            open_github()
        elif 'discord' in tokens:
            open_discord()
        elif 'gmail' in tokens:
            open_gmail()
    elif 'play' in tokens:
        if 'tech' in tokens and 'burner' in tokens:
            play_tech_burner()
        elif 'kaushik' in tokens and 'shresth' in tokens:
            play_kaushik_shresth()
        elif 'favourite' in tokens and 'videos' in tokens:
            play_my_favourite_videos()
        elif 'song' in tokens:
            play_song(query)
    elif 'time' in tokens:
        tell_time()
    elif 'notepad' in tokens:
        open_notepad()
    elif 'command' in tokens and 'prompt' in tokens:
        open_command_prompt()
    elif 'message' in tokens:
        send_message()
    elif 'joke' in tokens:
        tell_joke()
    elif 'location' in tokens:
        get_location()
    elif 'screenshot' in tokens:
        take_screenshot()
    elif 'system' in tokens and 'info' in tokens:
        get_system_info()
    elif 'volume' in tokens:
        if 'set' in tokens:
            speak("What level do you want to set the volume to?")
            level = takeCommand().strip()
            try:
                level = int(level)
                set_volume(level)
            except ValueError:
                speak("Invalid volume level.")
    elif 'files' in tokens:
        search_files(query)
    elif 'cookie' in tokens:
        if 'store' in tokens:
            speak("What key and value do you want to store in cookies?")
            key = takeCommand().strip()
            value = takeCommand().strip()
            store_cookie(key, value)
        elif 'retrieve' in tokens:
            speak("What key do you want to retrieve from cookies?")
            key = takeCommand().strip()
            retrieve_cookie(key)
    elif 'scrape' in tokens:
        speak("Please provide the URL to scrape data from.")
        url = takeCommand().strip()
        scrape_data(url)
    else:
        speak("Accessing database...")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("If I am not wrong...")
            print(results)
            speak(results)
        except wikipedia.exceptions.DisambiguationError:
            speak("There are multiple results for that query. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find any results.")

def detect_double_clap():
    global listening
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        while listening:
            print("Listening for double clap...")
            audio = r.listen(source, timeout=1)
            try:
                result = r.recognize_google(audio, language='en-in')
                if "Open " in result.lower():
                    print("Clap detected!")
                    time.sleep(1)  # Short delay to distinguish double clap
                    audio = r.listen(source, timeout=1)
                    result = r.recognize_google(audio, language='en-in')
                    if "Open" in result.lower():
                        print("Double clap detected! Opening Jarvis...")
                        run_alpha()
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                continue

class JarvisApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Welcome to Jarvis Assistant", size_hint=(1, 0.2))
        layout.add_widget(self.label)
        self.button = Button(text="Activate Jarvis", size_hint=(1, 0.2))
        self.button.bind(on_press=self.activate_jarvis)
        layout.add_widget(self.button)
        return layout

    def activate_jarvis(self, instance):
        self.label.text = "Jarvis is listening..."
        # Animate label to provide visual feedback
        animation = Animation(font_size=40, duration=0.5) + Animation(font_size=30, duration=0.5)
        animation.repeat = True
        animation.start(self.label)
        threading.Thread(target=run_alpha).start()

if __name__ == "__main__":
    JarvisApp().run()
