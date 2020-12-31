import speech_recognition as sr
import pyttsx3 as sp
import pywhatkit
import datetime as dt
import wikipedia as wiki
import pyjokes
import requests, json

listener = sr.Recognizer()
speech = sp.init()

voices = speech.getProperty('voices')
speech.setProperty('voice', voices[1].id)
print("Hi! I am Bella.. your Personal Assistant. What can I do for you?")
speech.say("Hi! I am Bella.. your Personal Assistant. What can I do for you?")
speech.runAndWait()

def talk(command):
    speech.say(command)
    speech.runAndWait()

def take_command():
    with sr.Microphone() as source:
        print('Listening... ')
        voice = listener.listen(source)
        command = listener.recognize_google(voice)
        command = command.lower()
        if 'bela' in command:
            command = command.replace('bela', '')
            print(command)
            return command
        elif 'bella' in command:
            command = command.replace('bella', '')
            print(command)
            return command
        return '  '

def play_song(song):
    print('playing' + song)
    talk('playing' + song)
    pywhatkit.playonyt(song)

def whatsapp():
    contacts = {'bro': '+91XXX', 'dad': '+91XXX', 'mom': '+91XXX'}
    with sr.Microphone() as source:
        talk('Whom do you want to send the message?')
        voice = listener.listen(source)
        person = listener.recognize_google(voice)
        person = person.lower()
        talk("What's the message?")
        voice = listener.listen(source)
        message = listener.recognize_google(voice)
        message = message.lower()
        talk('Sending the message to' + person)
    pywhatkit.sendwhatmsg(contacts[person], message, dt.datetime.now().hour, dt.datetime.now().minute+1, wait_time=10)

def tell_time():
    time = dt.datetime.now().strftime('%I:%M %p')
    print('Current time is : ' + time)
    talk('Current time is : ' + time)

def NewsFromBBC():
    api_key="Your API Key"
    main_url = "https://newsapi.org/v1/articles?source=bbc-news&sortBy=top&apiKey=" + api_key
    open_bbc_page = requests.get(main_url).json() 
    article = open_bbc_page["articles"] 
    results = [] 
    for ar in article:
        results.append(ar["title"])
    for i in results:
        print(i)
        talk(i)

def weather():
    with sr.Microphone() as source:
        talk('Please input the City')
        voice = listener.listen(source)
        city = listener.recognize_google(voice)
        city = city.lower()
    api_key="Your API Key"
    url = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + api_key
    x = requests.get(url).json()
    y = x["main"]
    current_temperature = y["temp"]-273 
    current_temperature = round(current_temperature, 2)
    print("It is currently " + str(current_temperature) + " degree celcius in " + city)
    talk("It is currently " + str(current_temperature) + " degree celcius in " + city)

def run_bella():
    command = take_command()
    if 'play' in command:
        song = command.replace('play', '')
        play_song(song)
    elif 'time' in command:
        tell_time()
    elif 'send' and 'whatsapp' in command:
        whatsapp()
    elif 'who is' in command:
        person = command.replace('who is', '')
        info = wiki.summary(person, 1)
        print(info)
        talk(info)
    elif 'weather' in command:
        weather()
    elif 'news' in command:
        NewsFromBBC()
    elif 'joke' in command:
        talk(pyjokes.get_joke())
    elif 'who created you' in command:
        talk("I was created by Kanak on December 19, 2020")
    else:
        talk("Sorry! I didn't understand that. Can you please say it again")
        run_bella()

while True:
    run_bella()