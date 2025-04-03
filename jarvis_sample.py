import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import pyaudio
import requests

# Set your email  here
EMAIL_ADDRESS = '*************'
EMAIL_PASSWORD = '************'

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    # Use the text-to-speech engine to speak the provided text
    engine.say(text)
    engine.runAndWait()

def wish_me():
    # Function to wish the user based on the current time
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hey Good morning !")
    elif 12 <= hour < 18:
        speak("Hey Good afternoon !")
    else:
        speak("Hey Good evening !")
    speak("I am Jarvis. How can I assist you today?")

def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 2
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print("You:", query)
            return query.lower()
        except Exception as e:
            print(e)
            speak("Sorry, I didn't get that.")
            return ""

def send_email(receiver, subject, message):
    # Function to send an email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, receiver, f"Subject: {subject}\n\n{message}")
        server.close()
        speak("Email sent successfully!")
    except Exception as e:
        print(e)
        speak("Sorry, I am unable to send the email at the moment.")

def shutdown():
    os.system("shutdown /s /t 1")
def restart():
    os.system("restart /s /t 1")

def fetch_news(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey=b32018f10dcb4036b43864df540c7119"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles')
        if articles:
            for idx, article in enumerate(articles, start=1):
                print(f"{idx}. {article['title']}")
                print(f"   {article['description']}")
                print(f"   Read more: {article['url']}")
                print()
        else:
            print("No articles found.")
    else:
        print("Failed to fetch news.")
def main():
    api_key = 'YOUR_NEWS_API_KEY'
    fetch_news(api_key)



def jarvis():
    wish_me()
    while True:
        query = take_command().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")
        elif 'open google chrome' in query:
            webbrowser.open("https://www.googlechrome.com")
        elif 'open svit atp' in query:
            webbrowser.open("https://www.svitatp.ac.in")
        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")
        elif 'the time' in query:
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {current_time}")
        elif 'i love you' in query:
            speak(f" i love you too jaaveed sir.but sorry sir i am not a human.i am your personal assistant")
        elif 'send email' in query:
            speak("Whom do you want to send the email to?")
            receiver = take_command().lower()
            speak("What should be the subject of the email?")
            subject = take_command().lower()
            speak("What should be the content of the email?")
            message = take_command().lower()
            send_email(receiver, subject, message)
        elif 'show me the live news updates' in query:
            speak("PLease click the given link to live news updates which you want to read...!")
            main()
        elif 'shut down my pc' in query:
            speak("shutting your pc...!")
            shutdown()
        elif 'restart my pc' in query:
            speak("Restrating your pc...!")
            restart()
        elif 'break' in query:
            speak("Goodbye! Have a great day!")
            break
        else:
            speak("I'm sorry, I don't understand that command.")

if __name__ == "__main__":
    jarvis()
