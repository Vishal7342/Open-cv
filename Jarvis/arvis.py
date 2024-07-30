from Body.Speak import SpeakW
from Body.Listen import Listen

def MainExe():
    text = "Main Execution Has Been Started"
    SpeakW(text)
    
    while True:
        query = Listen()
        
        if "hello" in query:
            SpeakW("Hi! I am Jarvis!")
            
        elif "bye" in query:
            SpeakW("Goodbye.")
            break

if __name__ == "__main__":
    MainExe()
