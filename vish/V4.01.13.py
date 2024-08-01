from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import pyttsx3
import datetime
import webbrowser
import os
import pywhatkit
import random
import pyjokes
import pyautogui
import speech_recognition as sr
import wikipedia
import requests
import threading
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import time

# Initialize text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    print(f"Speaking: {audio}")  # Debug statement
    engine.say(audio)
    engine.runAndWait()

def download_nltk_resources():
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        print("Downloading wordnet...")
        nltk.download('wordnet')
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading punkt...")
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        print("Downloading stopwords...")
        nltk.download('stopwords')

# Download necessary NLTK resources
download_nltk_resources()

# Initialize NLTK components
lemmatizer = WordNetLemmatizer()

def process_text(text):
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
    return tokens

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

def run_alpha():
    query = takeCommand()
    if query == "none":
        return

    tokens = process_text(query)
    
    if 'jarvis' in tokens:
        speak("Jarvis is now awake. How can I help you?")
        while True:
            query = takeCommand()
            if query == "none":
                continue
            
            tokens = process_text(query)
            if 'wikipedia' in tokens:
                speak('Searching Wikipedia...')
                query = ' '.join(tokens).replace("wikipedia", "").strip()
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError:
                    speak("There are multiple results for that query. Please be more specific.")
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find any results.")
            
            elif 'open' in tokens:
                if 'youtube' in tokens:
                    speak('Opening YouTube...')
                    webbrowser.open("https://www.youtube.com")
                elif 'google' in tokens:
                    speak('Opening Google...')
                    webbrowser.open("https://www.google.com")
                elif 'github' in tokens:
                    speak('Opening GitHub...')
                    webbrowser.open("https://www.github.com")
                elif 'discord' in tokens:
                    speak('Opening Discord...')
                    webbrowser.open("https://discord.com")
                elif 'gmail' in tokens:
                    speak("Opening Gmail...")
                    webbrowser.open("https://mail.google.com")
                elif 'tech burner' in tokens:
                    speak("Playing Tech Burner...")
                    webbrowser.open("https://www.youtube.com/@TechBurner")
                elif 'kaushik shresth' in tokens:
                    speak("Playing Kaushik Shresth...")
                    webbrowser.open("https://www.youtube.com/@Kaushikshresth")
                elif 'favourite videos' in tokens:
                    speak("Playing your favourite videos...")
                    webbrowser.open("https://www.youtube.com/@RAAAZofficial")
            
            elif 'time' in tokens:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")
            
            elif 'notepad' in tokens:
                speak('Opening Notepad...')
                nPath = "C:\\Program Files\\Notepad++\\notepad++.exe"
                if os.path.exists(nPath):
                    os.startfile(nPath)
                else:
                    speak("Notepad++ is not installed in the default path.")
            
            elif 'command prompt' in tokens:
                speak('Opening Command Prompt...')
                os.system('start cmd')
            
            elif 'send message' in tokens:
                speak('Sending message...')
                pywhatkit.sendwhatmsg('number here', 'message here', "time here")
            
            elif 'play' in tokens:
                song = ' '.join(tokens).replace('play', '').strip()
                speak(f'Playing {song}')
                webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
            
            elif "what's up" in tokens or 'how are you' in tokens:
                stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am full of energy', 'I am okay! How are you?']
                ans_q = random.choice(stMsgs)
                speak(ans_q)
                ans_take_from_user_how_are_you = takeCommand().lower()
                if 'fine' in ans_take_from_user_how_are_you or 'happy' in ans_take_from_user_how_are_you or 'okay' in ans_take_from_user_how_are_you:
                    speak('Okay...')
                elif 'not' in ans_take_from_user_how_are_you or 'sad' in ans_take_from_user_how_are_you or 'upset' in ans_take_from_user_how_are_you:
                    speak('Oh sorry...')
            
            elif 'made you' in tokens or 'created you' in tokens or 'developed you' in tokens:
                ans_m = "For your information, Mr. Arinjoy Acharya created me. I give a lot of thanks to him."
                print(ans_m)
                speak(ans_m)
            
            elif "hello" in tokens or "hello jarvis" in tokens:
                hel = "Hello Sir! How may I help you?"
                print(hel)
                speak(hel)
            
            elif "your name" in tokens:
                na_me = "Thanks for asking my name. My name is Jarvis."
                print(na_me)
                speak(na_me)
            
            elif "you feeling" in tokens:
                speak("Feeling very energetic after meeting with you.")
            
            elif "shut up" in tokens:
                speak("Sorry???")
                App.get_running_app().stop()
                return
            
            elif "not feeling well" in tokens:
                speak("WAIT... Take a deep breath, don't worry...")
                webbrowser.open('https://www.google.com/search?q=doctors+near+me')
            
            elif "i have fever" in tokens:
                speak("Take Calpol 650 or 500 according to your health and drink lots of water. You will feel better.")
            
            elif "ip address" in tokens:
                try:
                    ip = requests.get('https://api.ipify.org').text
                    speak(f"Your IP address is {ip}")
                except requests.RequestException:
                    speak("Sorry, I couldn't retrieve your IP address.")
            
            elif "tell me a joke" in tokens:
                joke = pyjokes.get_joke()
                speak(joke)
            
            elif "location" in tokens:
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
            
            elif "take a screenshot" in tokens:
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

            elif "sleep" in tokens:
                speak("Going back to sleep mode...")
                break

            else:
                speak("Accessing database...")
                # Add code to search the internet or local databases if needed
                speak("Sorry, I couldn't find any results.")

class JarvisApp(App):
    def build(self):
        self.title = 'Jarvis'
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text='Say something!', font_size='20sp', size_hint_y=None, height=50)
        layout.add_widget(self.label)
        self.text_input = TextInput(size_hint_y=None, height=40)
        layout.add_widget(self.text_input)
        return layout

    def on_start(self):
        # Start listening in the background
        self.listen_thread = threading.Thread(target=self.listen_loop, daemon=True)
        self.listen_thread.start()

    def listen_loop(self):
        while True:
            query = takeCommand()
            if query != "none":
                tokens = process_text(query)
                if 'jarvis' in tokens:
                    self.label.text = "Jarvis is awake. How can I help you?"
                    run_alpha()
                else:
                    self.label.text = "Jarvis is sleeping..."
            time.sleep(1)  # Add a delay to prevent excessive CPU usage

if __name__ == '__main__':
    JarvisApp().run()
