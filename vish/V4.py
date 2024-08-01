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
from http.cookies import SimpleCookie
from bs4 import BeautifulSoup
import requests
import re

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
    speak(f"Stored {key} in cookies.")

def retrieve_cookie(key):
    value = cookies.get(key)
    if value:
        speak(f"Retrieved {key}: {value.value}")
    else:
        speak(f"No data found for {key}.")

def scrape_data(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        data = soup.get_text()
        speak(f"Scraped data from {url}.")
        return data
    except Exception as e:
        speak(f"Failed to scrape data: {str(e)}")
        return ""

def run_alpha():
    query = takeCommand()
    if query == "none":
        return

    if 'wikipedia' in query:
        search_wikipedia(query)
    elif 'open youtube' in query:
        open_youtube()
    elif 'open google' in query:
        open_google()
    elif 'open github' in query:
        open_github()
    elif 'open discord' in query:
        open_discord()
    elif 'search on google' in query:
        search_on_google()
    elif 'open gmail' in query:
        open_gmail()
    elif 'play tech burner' in query:
        play_tech_burner()
    elif 'play kaushik shresth' in query:
        play_kaushik_shresth()
    elif 'play my favourite videos' in query:
        play_my_favourite_videos()
    elif 'the time' in query:
        tell_time()
    elif 'open notepad' in query:
        open_notepad()
    elif 'open command prompt' in query:
        open_command_prompt()
    elif 'send message' in query:
        send_message()
    elif 'play a song' in query:
        play_song(query)
    elif "what's up" in query or 'how are you' in query:
        whats_up()
    elif 'made you' in query or 'created you' in query or 'developed you' in query:
        who_made_you()
    elif "hello" in query or "hello jarvis" in query:
        say_hello()
    elif "your name" in query:
        your_name()
    elif "you feeling" in query:
        how_feeling()
    elif "shut up" in query:
        shut_up()
    elif "not feeling well" in query:
        not_feeling_well()
    elif "i have fever" in query:
        have_fever()
    elif 'ip address' in query:
        ip_address()
    elif 'tell me a joke' in query:
        tell_joke()
    elif 'where are we' in query:
        get_location()
    elif 'take screenshot' in query:
        take_screenshot()
    elif 'system info' in query:
        get_system_info()
    elif 'set volume' in query:
        speak("What level do you want to set the volume to?")
        level = takeCommand().strip()
        try:
            level = int(level)
            set_volume(level)
        except ValueError:
            speak("Invalid volume level.")
    elif 'search for files' in query:
        search_files(query)
    elif 'store cookie' in query:
        speak("What key and value do you want to store in cookies?")
        key = takeCommand().strip()
        value = takeCommand().strip()
        store_cookie(key, value)
    elif 'retrieve cookie' in query:
        speak("What key do you want to retrieve from cookies?")
        key = takeCommand().strip()
        retrieve_cookie(key)
    elif 'scrape data' in query:
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
        threading.Thread(target=run_alpha).start()

if __name__ == "__main__":
    JarvisApp().run()
