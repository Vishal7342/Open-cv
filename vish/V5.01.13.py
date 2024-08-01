import numpy as np
import pyaudio
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

# Kivy Imports
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

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
                speak("Screenshot saved successfully.")
            
            elif "search the web" in tokens:
                search_query = ' '.join(tokens).replace('search the web', '').strip()
                if search_query:
                    speak(f"Searching the web for {search_query}")
                    webbrowser.open(f"https://www.google.com/search?q={search_query}")
                else:
                    speak("Please provide a search query.")
            
            else:
                speak("Sorry, I couldn't find any results.")

def detect_double_clap():
    # Parameters for audio detection
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 5000
    CLAP_DURATION = 0.5  # Duration to consider for each clap in seconds
    MIN_CLAP_INTERVAL = 0.5  # Minimum interval between claps in seconds

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    print("Listening for double clap...")

    clap_count = 0
    last_clap_time = time.time()
    listening = False

    try:
        while True:
            data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
            peak = np.max(np.abs(data))
            
            if peak > THRESHOLD:
                current_time = time.time()
                if current_time - last_clap_time < MIN_CLAP_INTERVAL:
                    clap_count += 1
                else:
                    clap_count = 1  # Reset count if the interval is too long
                
                last_clap_time = current_time
                
                if clap_count == 2:
                    if not listening:
                        print("Double clap detected! Activating Jarvis...")
                        speak("Jarvis is now awake. How can I help you?")
                        listening = True
                        run_alpha()
                        clap_count = 0  # Reset clap count after detection
                else:
                    listening = False  # Reset if not double clap
            time.sleep(0.1)  # Add a delay to reduce CPU usage

    except KeyboardInterrupt:
        print("Terminating...")
        stream.stop_stream()
        stream.close()
        p.terminate()

class JarvisApp(App):
    def build(self):
        Window.clearcolor = (0.2, 0.2, 0.2, 1)  # Set background color
        layout = FloatLayout()
        
        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        self.label = Label(
            text='Welcome to Jarvis',
            font_size='32sp',
            size_hint=(None, None),
            size=(Window.width * 0.9, 50),
            pos_hint={'center_x': 0.5, 'top': 0.9},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(self.label)
        
        self.text_input = TextInput(
            size_hint=(None, None),
            size=(Window.width * 0.8, 40),
            pos_hint={'center_x': 0.5, 'center_y': 0.7},
            multiline=False,
            hint_text='Type your command here...',
            background_color=(0.1, 0.1, 0.1, 1),
            foreground_color=(1, 1, 1, 1)
        )
        layout.add_widget(self.text_input)
        
        self.sleep_switch = Switch(
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.6}
        )
        self.sleep_switch.bind(active=self.on_sleep_switch)
        layout.add_widget(self.sleep_switch)
        
        self.sleep_status_label = Label(
            text='Jarvis is awake',
            font_size='20sp',
            size_hint=(None, None),
            size=(Window.width * 0.5, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.55},
            color=(1, 1, 1, 1)
        )
        layout.add_widget(self.sleep_status_label)
        
        self.screenshot_button = Button(
            text='Take Screenshot',
            size_hint=(None, None),
            size=(200, 50),
            pos_hint={'center_x': 0.5, 'center_y': 0.4},
            background_color=(0.1, 0.5, 0.8, 1)
        )
        self.screenshot_button.bind(on_press=self.take_screenshot)
        layout.add_widget(self.screenshot_button)
        
        return layout

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def on_start(self):
        self.clap_thread = threading.Thread(target=detect_double_clap, daemon=True)
        self.clap_thread.start()

    def on_sleep_switch(self, instance, value):
        if value:
            self.sleep_status_label.text = 'Jarvis is awake'
        else:
            self.sleep_status_label.text = 'Jarvis is asleep'
            self.clap_thread = threading.Thread(target=detect_double_clap, daemon=True)
            self.clap_thread.start()

    def take_screenshot(self, instance):
        speak("Please tell me the name for the screenshot file.")
        name = takeCommand().strip()
        if name == "none":
            speak("Screenshot name not provided.")
            return
        speak("Taking screenshot...")
        time.sleep(2)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        speak("Screenshot saved successfully.")

if __name__ == '__main__':
    JarvisApp().run()
