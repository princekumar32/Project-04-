import os
import subprocess
import speech_recognition as sr
import pyttsx3
import webbrowser
from musiclibrary import music  # import your music library 
import requests
import datetime  # Added datetime module
from client import ask_gpt

# Set audio driver for Linux (ALSA)
os.environ["SDL_AUDIODRIVER"] = "alsa"

recognizer = sr.Recognizer()
engine = pyttsx3.init()
# Use your News API key here
newsapi ="sk.."

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    print("Recording for 3 seconds...")
    subprocess.run([
        "arecord", "-D", "plughw:1,0", "-f", "cd", "-t", "wav",
        "-d", "3", "-r", "44100", "command.wav"
    ])
    with sr.AudioFile("command.wav") as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text.lower()
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError as e:            # Listen briefly for stop command

        print(f"API Error: {e}")
        return ""
    
def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        if not articles:
            speak("Sorry, I couldn't find any news right now.")
            return

        speak("Starting Us news headlines. Say 'stop news' to exit.")
        for i, article in enumerate(articles, 1):
            title = article.get("title", "No title")
            speak(f"Headline {i}: {title}")

            # Listen briefly for stop command
            speak("Say 'stop news' to stop, or wait for next headline.")
            command = listen()
            if "stop news" in command:
                speak("Stopping the news reading.")
                break

    except requests.exceptions.RequestException as e:
        speak("There was a problem fetching the news.")
        print(f"News API error: {e}")



if __name__ == "__main__":
    speak("Initializing Jarvis...")
    while True:
        command = listen()
        if not command:
            continue

        # Wake word
        if "jarvis" in command:
            jarvis_active = True
            speak("Jarvis is active. What can I do for you?")
            continue

        # Stop Jarvis
        if "stop jarvis" in command:
            jarvis_active = False 
            speak("Jarvis deactivated.")
            continue

        # Ignore other commands unless activated
        if not jarvis_active:
            continue


        if "stop" in command:
            speak("Goodbye!")
            break
        elif "youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "google" in command:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "linkedin" in command:
            speak("Opening LinkedIn")
            webbrowser.open("https://www.linkedin.com")
        elif "github" in command:
            speak("Opening GitHub")
            webbrowser.open("https://www.github.com")
        elif "twitter" in command:
            speak("Opening Twitter")
            webbrowser.open("https://www.twitter.com")
        elif command.lower().startswith("play"):
            song = command.lower().replace("play ", "").strip()

            if song in music:
                speak(f"Playing {song}")
                webbrowser.open(music[song])
            else:
                speak(f"Searching for {song} on YouTube")
                webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
        
        elif "news" in command:
            get_news()

        elif "time" in command:
            current_time = datetime.datetime.now().strftime("%I:%M %p")
            message = f"The current time is {current_time}"
            print(message)
            speak(message)

        elif "date" in command:
            today = datetime.date.today()
            message = f"Today's date is {today.strftime('%B %d, %Y')}"
            print(message)
            speak(message)

        elif "day" in command:
            day_name = datetime.datetime.now().strftime("%A")
            message = f"Today is {day_name}"
            print(message)
            speak(message)
        
        elif "what is" in command or "who is" in command or "explain" in command:
            answer = ask_gpt(command)
            speak(answer)
            

        else:
            speak("I didn't catch a known command.")
            