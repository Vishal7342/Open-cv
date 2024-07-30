# import speech_recognition as sr
# import os
from Features.Clap import Tester

# def Listen():

#     r = sr.Recognizer()

#     with sr.Microphone() as source:
#         print("Listening...")
#         r.pause_threshold = 1
#         audio = r.listen(source,0,8) # Listening Mode.....
    
#     try:
#         print("Recognizing...")
#         query = r.recognize_google(audio,language="en")

#     except:
#         return ""
    
#     query = str(query).lower()
#     print(query)
#     return query

# def WakeupDetected():
#         queery = Listen().lower()

#         if "wake up" in queery:
#             print("weke up Detected")
#             MainExe()
        
#         else:
#             pass
 
# while True:
#     WakeupDetected()       
        
        
# # def Main():
# #     Tester()
# #     Speak("hi")
# #     # Ensure the driver is closed properly
# #     from Body.a import close_driver
# #     close_driver()

# # if __name__ == "__main__":
# #     Main()
 
 
data = Tester()
if "True=Mic" == data:
    from arvis import MainExe
    MainExe()
    
    from Body.a import close_driver
    close_driver()