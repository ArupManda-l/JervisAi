import pyautogui
import speech_recognition as sr
import pyttsx3
import datetime
import os
import cv2
from requests import get
import time
import sys
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
import time
import smtplib

# Initialize pyttsx3 engine for text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Set the voice to the first available voice


# Text-to-speech function
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# Function to take voice commands
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        r.phrase_threshold = 0.3
        r.energy_threshold = 300

        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing.....")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
        except sr.WaitTimeoutError:
            speak("Sorry, I didn't hear anything. Please try again.")
            return "none"
        except sr.RequestError as e:
            speak("Sorry, there was an error with the speech service.")
            print(f"Error: {e}")
            return "none"
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
            return "none"
        except Exception as e:
            speak(f"An error occurred: {e}")
            return "none"
    return query


# Wish function
def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good morning")
    elif hour >= 12 and hour <= 18:
        speak("Good evening")
    else:
        speak("Good night")


# Function to open camera
def open_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        speak("Sorry, I couldn't access the camera. Trying again...")
        cap = cv2.VideoCapture(0)  # Retry opening the camera
        if not cap.isOpened():
            speak("Still unable to access the camera.")
            return False

    # If the camera is accessible, display the video feed
    speak("Camera is now on.")
    while True:
        ret, img = cap.read()
        if not ret:
            speak("Failed to grab frame from the camera.")
            break

        cv2.imshow('webcam', img)
        k = cv2.waitKey(50)
        if k == 27:  # Press 'Esc' to close the camera window
            break

    cap.release()
    cv2.destroyAllWindows()
    return True


# Main function
if __name__ == "__main__":
    wish()
    speak("Hello, I am Jervis. How can I assist you?")


    while True:
        query = takecommand().lower()

        if "open notepad" in query:
            npath = "C:\\Windows\\notepad.exe"
            os.startfile(npath)

        elif "open command prompt" in query:
            os.system("start cmd")

        elif "open camera" in query:
            open_camera()

        elif "please tell me my ip address " in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
                print(results)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"Multiple results found. Please be more specific. Example: {e.options[:3]}")
            except wikipedia.exceptions.HTTPTimeoutError:
                speak("Sorry, there was a timeout while connecting to Wikipedia.")
            except wikipedia.exceptions.RedirectError:
                speak("Redirect error occurred.")
            except Exception as e:
                speak(f"An error occurred: {e}")

        elif "open youtube" in query:
            webbrowser.open("www.youtube.com")
        elif "open facebook" in query:
            webbrowser.open("www.facebook.com")
        elif "open instagram" in query:
            webbrowser.open("www.instagram.com")
        elif "open google" in query:
            speak("What should I search on Google?")
            search_query = takecommand().lower()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")

        elif "send message" in query:
            pywhatkit.sendwhatmsg("+918017595759", "I am Jervis", 6, 30)

        elif "play songs on youtube" in query:
            pywhatkit.playonyt("Daspasito")


        elif "close youtube" in query:
            speak("Closing YouTube now.")
            pyautogui.hotkey('ctrl', 'w')  # Close current browser tab
            # Alternatively, close the entire browser:
            # os.system("taskkill /f /im chrome.exe")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "shutdown the system" in query:
            os.system("shutdown /s /f /t 1")  # Shutdown system after 1 second

        elif "restart the system" in query:
            os.system("shutdown /r /f /t 1")  # Restart system after 1 second

        elif "switch the window" in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(1)
            pyautogui.keyUp("alt")

        # Exit loop if "no more work left" is said
        elif "no more work left" in query:
            speak("Thanks for using me. Have a good day.")
            sys.exit()
