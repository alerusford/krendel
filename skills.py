import os
import webbrowser
import sys
import requests
import subprocess
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 180)

def speaker(text):
    engine.say(text)
    engine.runAndWait()

def browser():
    webbrowser.open('http://youtube.com', new=2)

def game():
    subprocess.run('C:/Users/alexandr/Desktop/game.txt')

def offpc():
    print(' - пк выключен!')

def weather():
    print(' - погода!')

    api_key = 'e90ff88039119e31365efe5760a1b750'
    params = {'q': 'Kolomna', 'units': 'metric', 'lang': 'ru', 'appid': api_key}
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
    w = response.json()
    print(w)
    print(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])}")
    speaker(f"На улице, {w['weather'][0]['description']}, {round(w['main']['temp'])}")

def offBot():
    sys.exit()

def passive():
    pass