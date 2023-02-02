import config
import stt
import tts
import datetime
from num2words import num2words
import webbrowser
import requests

# from fuzzywuzzy import fuzz
# import random

print(f"{config.VA_NAME} начал свою работу ...")

def va_respond(voice: str):
    print(' - вопрос: ', voice)
    if voice.startswith(config.VA_ALIAS):
        # cmd = recognize_cmd(filter_cmd(voice))
        cmd = filter_cmd(voice)
        print(' - va_respond cmd: ', cmd)
        cmd_split = cmd.split()

        if cmd == 'тест':
            print(' - ТЕСТ! - ')

        elif 'найди' in cmd_split:
            print(' - cmd_split: ', cmd_split)
            print(' - запускаем чат бот!')

        for k, v in config.VA_CMD_LIST.items():
            if cmd in v:
                print(' - find! key: ', k)
                execute_cmd(k)

        # else:
        #     print(' - Что?')
        #     tts.va_speak("Что?")


def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    print(' - cmd: ', cmd)
    return cmd


# def recognize_cmd(cmd: str):
#     print(' - recognize_cmd: ', cmd)
#     rc = {'cmd': '', 'percent': 0}
#     for c, v in config.VA_CMD_LIST.items():
#         for x in v:
#             # vrt = fuzz.ratio(cmd, x)
#             vrt = cmd, x
#             print(' - vrt:', vrt)
#             if vrt > rc['percent']:
#                 rc['cmd'] = c
#                 rc['percent'] = vrt
#     print(' - rc: ', rc)
#     return rc
    # print(cmd)
    # return cmd


def execute_cmd(cmd: str):


    if cmd == 'help':
        print(' - execute_cmd help: ', cmd)
        # help
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "рассказывать анекдоты ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass

    elif cmd == 'ctime':
        print(' - execute_cmd ctime: ', cmd)
        # current time
        now_hours = num2words(datetime.datetime.now().hour, lang='ru')
        now_minutes = num2words(datetime.datetime.now().minute, lang='ru')
        text = "Сейчас " + now_hours + ' ' + now_minutes
        print(' - ответ: ', text)
        tts.va_speak(text)

    elif cmd == 'open_browser':
        webbrowser.open("http://python.org")

    elif cmd == 'weather':
            params = {'q': 'Kolomna', 'units': 'metric', 'lang': 'ru', 'appid': config.api_key}
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
            w = response.json()
            print(w)
            gradus = num2words(round(w['main']['temp']), lang='ru')
            print(' - gradus: ', gradus)
            print(f"На улице {w['weather'][0]['description']} {gradus}")
            tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus} градуса.")


# прослушивание
stt.va_listen(va_respond)
