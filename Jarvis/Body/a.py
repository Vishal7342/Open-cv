import pyttsx3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from time import sleep
import chromedriver_autoinstaller

# Ensure the latest version of chromedriver is installed
chromedriver_autoinstaller.install()

# Chrome-based TTS using ttsmp3.com
chrome_options = Options()
chrome_options.add_argument('--log-level=3')
chrome_options.headless = True  # Set to True for headless mode, False for GUI mode
service = Service()
driver = None

def initialize_driver():
    global driver
    if driver is None:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        website = r"https://ttsmp3.com/text-to-speech/British%20English/"
        driver.get(website)
        # Select the voice (optional, can be skipped if default is fine)
        ButtonSelection = Select(driver.find_element(By.ID, 'sprachwahl'))
        ButtonSelection.select_by_visible_text('British English / Brian')

def Speak(Text):
    if driver is None:
        initialize_driver()

    length_of_text = len(str(Text))
    if length_of_text == 0:
        print("No text provided.")
        return

    try:
        print(f"AI: {Text}")
        Data = str(Text)
        xpath_of_textarea = '//*[@id="voicetext"]'
        
        # Clear the text area
        textarea = driver.find_element(By.XPATH, value=xpath_of_textarea)
        textarea.clear()
        
        # Send keys to the text area
        textarea.send_keys(Data)
        print("Text entered into the textarea.")

        # Click the play button
        play_button = driver.find_element(By.ID, 'vorlesenbutton')
        play_button.click()
        print("Play button clicked.")

        # Adjust sleep time based on text length
        if length_of_text >= 100:
            sleep(13)
        elif length_of_text >= 70:
            sleep(10)
        elif length_of_text >= 55:
            sleep(8)
        elif length_of_text >= 40:
            sleep(6)
        elif length_of_text >= 30:
            sleep(4)
        else:
            sleep(2)
        
        # Ensure the play button isn't clicked again
        sleep(4)
        driver.execute_script("arguments[0].blur();", play_button)

    except Exception as e:
        print(f"Error during Speak execution: {e}")

# Ensure cleanup of the WebDriver when done
def close_driver():
    global driver
    if driver is not None:
        driver.quit()
        driver = None
