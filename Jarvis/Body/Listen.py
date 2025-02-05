# Hindi or English - Command
# English

# step - 1
# pip install googletrans==3.1.0a0

# step - 2
# Three function
# 1 - Listwn Function
# 2 - English tranlation
# 3 - Connect 

import speech_recognition as sr #pip install speechrecognition
from googletrans import Translator  # pip install googlr

# 1 - Listen : Hindi or English

def Listen():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source,0,8)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio,language="en")

    except:
        return ""

    query = str(query).lower()
    return query

# 2 - Translation

def TranslationHinToEng(Text):
    line = str(Text)
    translate = Translator()
    result = translate.translate(line)
    data = result.text
    print(f"You : {data}")
    return data

# 3 - Connect

def MicExecution():
    query = Listen()
    data = TranslationHinToEng(query)
    return data
