import pyjokes
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import csv
import pygame
from PIL import Image, ImageTk
import requests
import urllib.parse
import webbrowser
import random
import tkinter as tk
from tkinter import Canvas, Frame, Scrollbar

engine=pyttsx3.init()

def speak(audio):
    engine.setProperty('rate', 150)
    engine.say(audio)
    engine.runAndWait()
    print("Assistant:", audio)
    update_conversation(audio, "Assistant")

def play_youtube_song():
    speak("What song would you like to listen to dear user?")
    song_name = takeCommand().lower()
    query = urllib.parse.quote(song_name)
    url = f"https://www.youtube.com/results?search_query={query}"
    response = requests.get(url)
    content = response.content.decode("utf-8")
    start = content.find("watch?v=")
    end = content.find("\"", start)
    video_id = content[start:end]
    video_url = f"https://www.youtube.com/{video_id}"
    webbrowser.open(video_url)

    speak("Now playing {song_name} on YouTube.")

def clear_Wholecalendar():
    open("calendar.csv", "w").close()

    print("Takvim etkinlikleri temizlendi!")
def clean_calendar():
    today = datetime.date.today()
    with open("calendar.csv", "r") as file:
        reader = csv.reader(file)
        rows = []
        for row in reader:
            date_str = row[0]
            day, month, year = map(int, date_str.split("/"))
            date = datetime.date(year, month, day)
            if date >= today:
                rows.append(row)
    with open("calendar.csv", "w", newline='') as file:
        writer = csv.writer(file)
        for row in rows:
            writer.writerow(row)
            speak("Ada updated your calendar")
def view_calendar():
    speak("There is your calendar")
    with open("calendar.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
            speak(row)
def calendar():
    speak("What's your plan?")
    plan = takeCommand().lower()
    speak("Choose a date for your plan day/month/year")
    while True:
        try:
            speak("choose the day!!!")
            day = takeCommand().lower()
            speak("choose the month!!!")
            month = takeCommand().lower()
            speak("choose the year!!!")
            year = takeCommand().lower()
            selected_date = datetime.date(year, month, day)
            if selected_date < datetime.date.today():
                speak("Try a valid date! Try again")
            else:
                break
        except ValueError:
            speak("Try a valid date! Try again")
    with open("calendar.csv", "a") as file:
        file.write("{}/{}/{}".format(day, month, year))
        file.write(plan)
        speak("Added to your calendar!")
def stop():
    speak("The system is stoping...")
def get_daily_quote():
    quotes = [
        "Religion is excellent stuff for keeping common people quiet. Religion is what keeps the poor from murdering the rich.",
        "Whatever possession we gain by our sword cannot be sure or lasting, but the love gained by kindness and moderation is certain and durable.",
        "To see me does not necessarily mean to see my face. To understand my thoughts is to have seen me."
    ]

    speakers = [
        "Napoleon Bonaparte",
        "Alexander the Great",
        "Mustafa Kemal Ataturk"

    ]

    selected_index = random.randint(0, len(quotes) - 1)
    selected_quote = quotes[selected_index]
    speaker = speakers[selected_index]

    return selected_quote, speaker



def speak_daily_quote():
    quote, speaker = get_daily_quote()
    speak(f"Todays quote '{quote}' - {speaker}")

def time():
    Time = datetime.datetime.now().strftime("%I:%M:%S")
    speak("The current time is " + Time)
def made():
    speak("Thanks to Yunus and Zehra further It's a secret")
def love():
    audio_file_path = r"whatis.mp3"
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    pygame.quit()
    speak("Love, it's very hard to describe but a feeling that every person should experience.")
def date():
    year=int(datetime.datetime.now().year)
    month= int(datetime.datetime.now().month)
    day= int(datetime.datetime.now().day)
    speak("The current date is")
    speak(day)
    speak(month)
    speak(year)
def wishme():
    speak("Welcome back dear user!")
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        speak("Good morning!")
    elif hour >= 12 and hour < 18:
        speak("Good afternoon!")
    elif hour >= 18 and hour < 24:
        speak("Good evening!")
    else:
        speak("Good night!")
    speak("Ada is here for to help you. How can Ada help you?")
def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold=1
        audio=r.listen(source)
    try:
        print("Analyzing...")
        query=r.recognize_google(audio, language='en-in')
        print(query)
    except Exception as a:
        print(a)
        speak("Can you repeat it again?")
        return "None"
    return query
def jokes():
    speak(pyjokes.get_joke())
class SpeechBubble(tk.Canvas):
    def __init__(self, parent, text="", sender="User", **kwargs):
        super().__init__(parent, **kwargs)
        bg_color = "lightblue" if sender == "User" else "lightgreen"
        self.config(bg=bg_color, highlightthickness=0)
        self.create_text(10, 10, text=text, anchor="nw", fill="black", width=240)


def update_conversation(message, sender="User"):
    bubble = SpeechBubble(conversation_canvas, text=message, sender=sender, width=250, height=50)
    bubble.pack_propagate(False)
    if sender == "User":
        bubble.pack(side='top', anchor='e', padx=10, pady=5)
    else:
        bubble.pack(side='top', anchor='w', padx=10, pady=5)

    conversation_canvas.update_idletasks()
    conversation_canvas.yview_moveto(1)

def on_voice_command():
    user_input = takeCommand().lower()
    update_conversation(user_input, "User")
    process_command(user_input)
def process_command(query):
    try:
        if 'time'in query:
            time()
        elif 'date'in query:
            date()
        elif 'chrome'in query:
            speak("What are you looking for dear user?")
            chromepath = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
            search= takeCommand().lower()
            wb.get(chromepath).open_new_tab(search+'.com')
        elif 'wikipedia'in query:
            speak("Searching...")
            query = query.replace("wikipedia","")
            result= wikipedia.summary(query, sentences=2)
            print(result)
            speak(result)
        elif "who made you" in query:
            made()
        elif "what is love" in query:
            love()
        elif 'say something' in query:
            speak_daily_quote()
        elif 'remember that' in query:
            speak("What should Ada remember?")
            data= takeCommand()
            speak("You said that to me: "+data)
            remember = open('data.txt','w')
            remember.write(data)
            remember.close()
        elif 'do you know' in query:
            remember=open("data.txt", 'r')
            speak("You said that to me"+remember.read())
        elif 'add to calendar' in query:
            calendar()
        elif 'show the calendar' in query:
            view_calendar()
        elif 'edit the calendar'in query:
            clean_calendar()
        elif 'youtube' in query:
            play_youtube_song()
        elif 'joke' in query:
            jokes()
        elif 'clear the calendar'in query:
            clear_Wholecalendar()
        elif 'stop the system'in query:
            stop()
        else:
            update_conversation("I didn't understand that command.", "Assistant")

    except Exception as e:
        update_conversation("An error occurred: " + str(e), "Assistant")

last_bubble_y = 0
bubble_spacing = 5

root = tk.Tk()
root.title("Ada the Voice Assistant")
root.geometry("800x600")

background_image = Image.open("background.jpg")
background_image = background_image.resize((800, 600), Image.ANTIALIAS)
background_photo = ImageTk.PhotoImage(background_image)

conversation_canvas = Canvas(root, width=800, height=550)
conversation_canvas.pack(side='top', fill="both", expand=True)
conversation_canvas.create_image(0, 0, image=background_photo, anchor="nw")

scrollbar = Scrollbar(root, command=conversation_canvas.yview)
scrollbar.pack(side='right', fill='y')
conversation_canvas.configure(yscrollcommand=scrollbar.set)

voice_command_button = tk.Button(root, text="Speak", command=on_voice_command)
voice_command_button.pack(padx=10, pady=10)

wishme()

root.mainloop()