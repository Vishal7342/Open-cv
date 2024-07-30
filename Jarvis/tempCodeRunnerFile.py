from Body.a import Speak

def Main():
    Tester()
    Speak("hi")
    # Ensure the driver is closed properly
    from Body.a import close_driver
    close_driver()