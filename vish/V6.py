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
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def download_nltk_resources():
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet')
    
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')

# Download necessary NLTK resources
download_nltk_resources()

# Initialize NLTK components
lemmatizer = WordNetLemmatizer()

def process_text(text):
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalnum()]
    return tokens

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.5
        audio = r.listen(source, timeout=5)
    
    try:
        query = r.recognize_google(audio, language='en-in')
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I did not understand the audio.")
        return "none"
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")
        return "none"

def run_alpha(query):
    tokens = process_text(query)
    response = "I didn't understand that command."

    if 'jarvis' in tokens:
        response = "Jarvis is now awake. How can I help you?"
    
    elif 'wikipedia' in tokens:
        query = ' '.join(tokens).replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(query, sentences=2)
            response = f"According to Wikipedia: {results}"
        except wikipedia.exceptions.DisambiguationError:
            response = "There are multiple results for that query. Please be more specific."
        except wikipedia.exceptions.PageError:
            response = "Sorry, I couldn't find any results."
    
    elif 'open' in tokens:
        if 'youtube' in tokens:
            webbrowser.open("https://www.youtube.com")
            response = 'Opening YouTube...'
        elif 'google' in tokens:
            webbrowser.open("https://www.google.com")
            response = 'Opening Google...'
    
    elif 'time' in tokens:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        response = f"The time is {strTime}"
    
    elif 'notepad' in tokens:
        nPath = "C:\\Program Files\\Notepad++\\notepad++.exe"
        if os.path.exists(nPath):
            os.startfile(nPath)
            response = 'Opening Notepad...'
        else:
            response = "Notepad++ is not installed in the default path."
    
    elif 'command prompt' in tokens:
        os.system('start cmd')
        response = 'Opening Command Prompt...'
    
    elif 'send message' in tokens:
        pywhatkit.sendwhatmsg('number here', 'message here', "time here")
        response = 'Sending message...'
    
    elif 'play' in tokens:
        song = ' '.join(tokens).replace('play', '').strip()
        webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        response = f'Playing {song}'
    
    elif 'location' in tokens:
        try:
            ip = requests.get('https://api.ipify.org').text
            url = f'https://get.geojs.io/v1/ip/geo/{ip}.json'
            geo_requests = requests.get(url)
            geo_data = geo_requests.json()
            city = geo_data['city']
            state = geo_data['state']
            country = geo_data['country']
            response = f"We are in {city}, {state}, {country}."
        except Exception:
            response = "Sorry, I couldn't find your location."
    
    elif 'screenshot' in tokens:
        response = "Please tell me the name for the screenshot file."
        speak(response)
        name = take_command().strip()
        if name != "none":
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            response = "Screenshot saved successfully."
        else:
            response = "Screenshot name not provided."
    
    elif 'search the web' in tokens:
        search_query = ' '.join(tokens).replace('search the web', '').strip()
        if search_query:
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            response = f"Searching the web for {search_query}"
        else:
            response = "Please provide a search query."
    
    elif 'joke' in tokens:
        joke = pyjokes.get_joke()
        response = joke
    
    elif "how are you" in tokens:
        response = random.choice(['Just doing my thing!', 'I am fine!', 'Nice!', 'I am full of energy', 'I am okay! How are you?'])
    
    elif "hello" in tokens:
        response = "Hello Sir! How may I help you?"
    
    elif "your name" in tokens:
        response = "My name is Jarvis."
    
    elif "you feeling" in tokens:
        response = "Feeling very energetic after meeting with you."
    
    elif "shut up" in tokens:
        response = "Sorry???"
        App.get_running_app().stop()
    
    elif "not feeling well" in tokens:
        response = "WAIT... Take a deep breath, don't worry..."
        webbrowser.open('https://www.google.com/search?q=doctors+near+me')
    
    elif "i have fever" in tokens:
        response = "Take Calpol 650 or 500 according to your health and drink lots of water. You will feel better."
    
    elif "ip address" in tokens:
        try:
            ip = requests.get('https://api.ipify.org').text
            response = f"Your IP address is {ip}"
        except requests.RequestException:
            response = "Sorry, I couldn't retrieve your IP address."
    
    speak(response)
    return response

def detect_double_clap():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    THRESHOLD = 5000
    MIN_CLAP_INTERVAL = 0.5

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    clap_count = 0
    last_clap_time = time.time()
    listening = False

    while True:
        data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
        peak = np.max(np.abs(data))
        
        if peak > THRESHOLD:
            current_time = time.time()
            if current_time - last_clap_time < MIN_CLAP_INTERVAL:
                clap_count += 1
            else:
                clap_count = 1
            
            last_clap_time = current_time
            
            if clap_count == 2:
                if not listening:
                    speak("Jarvis is now awake. How can I help you?")
                    listening = True
                    run_alpha(take_command())
                    clap_count = 0
            else:
                listening = False
        time.sleep(0.1)

class JarvisApp(App):
    def build(self):
        self.title = 'Jarvis'
        layout = BoxLayout(orientation='vertical')

        # Header
        header = BoxLayout(size_hint_y=0.1, padding=10, spacing=10)
        header.add_widget(Image(source='chatgpt_logo.png', size_hint=(0.1, 1)))
        header.add_widget(Label(text="Jarvis Assistant", font_size=24, size_hint=(0.9, 1)))
        layout.add_widget(header)

        # Chat Box
        self.chat_box = ScrollView(size_hint=(1, 0.8))
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=10)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_box.add_widget(self.chat_layout)
        layout.add_widget(self.chat_box)

        # User Input
        self.text_input = TextInput(size_hint_y=None, height=40, multiline=False)
        self.text_input.bind(on_text_validate=self.on_enter)
        layout.add_widget(self.text_input)

        # Buttons
        button_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.sleep_switch = Switch(active=True)
        self.sleep_switch.bind(active=self.on_sleep_switch)
        button_layout.add_widget(self.sleep_switch)
        button_layout.add_widget(Button(text='Take Screenshot', on_press=self.take_screenshot))
        layout.add_widget(button_layout)

        self.status_label = Label(text='Jarvis is awake', font_size='20sp', size_hint_y=None, height=50)
        layout.add_widget(self.status_label)

        return layout

    def on_start(self):
        self.clap_thread = threading.Thread(target=detect_double_clap, daemon=True)
        self.clap_thread.start()

    def on_enter(self, instance):
        query = self.text_input.text
        response = run_alpha(query)
        self.add_message(f"You: {query}")
        self.add_message(f"Jarvis: {response}")
        self.text_input.text = ''

    def on_sleep_switch(self, instance, value):
        if value:
            self.status_label.text = 'Jarvis is awake'
        else:
            self.status_label.text = 'Jarvis is asleep'
            self.clap_thread = threading.Thread(target=detect_double_clap, daemon=True)
            self.clap_thread.start()

    def take_screenshot(self, instance):
        speak("Please tell me the name for the screenshot file.")
        name = take_command().strip()
        if name != "none":
            img = pyautogui.screenshot()
            img.save(f"{name}.png")
            speak("Screenshot saved successfully.")
        else:
            speak("Screenshot name not provided.")

    def add_message(self, message):
        label = Label(text=message, size_hint_y=None, height=40)
        self.chat_layout.add_widget(label)
        self.chat_box.scroll_to(label)

if __name__ == '__main__':
    JarvisApp().run()
