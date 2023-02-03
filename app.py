import config
import stt
import tts
from num2words import num2words
import webbrowser
import requests
import openai
import telebot
from telebot import types
import json
import traceback
import time
import os
from datetime import datetime
# from io import BytesIO
# from PIL import Image
# from fuzzywuzzy import fuzz
# import random
from threading import Thread

thisFile = os.path.abspath(__file__)
openai.api_key = config.openai_apikey
bot = telebot.TeleBot(config.telegram_apikey)

print(' - this is ', thisFile)

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
                break
            else:
                time_start = datetime.now()

                response = openai.Completion.create(
                    model='text-davinci-003',
                    prompt=cmd,
                    temperature=0.5,
                    max_tokens=2000,
                    top_p=1.0,
                    frequency_penalty=0.5,
                    presence_penalty=0.0,
                )

                answer_chatgpt = response['choices'][0]['text']
                print(' - вопрос: ', cmd)
                print(' - ответ: ', answer_chatgpt)
                print(' - ответ длина: ', len(answer_chatgpt))

                time_end = datetime.now()
                time_request = time_end - time_start
                print(' - время запроса:', time_request)
                # tts.va_speak(answer_chatgpt)
                # bot.send_message(chat_id=message.from_user.id, text=f"{response['choices'][0]['text']}")
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
        text += "узнавать погоду ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass

    elif cmd == 'ctime':
        print(' - execute_cmd ctime: ', cmd)
        # current time
        now_hours = num2words(datetime.now().hour, lang='ru')
        now_minutes = num2words(datetime.now().minute, lang='ru')
        text = "Сейчас " + now_hours + ' ' + now_minutes
        print(' - ответ: ', text)
        tts.va_speak(text)

    elif cmd == 'open_browser':
        webbrowser.open("http://python.org")

    elif cmd == 'weather':
            params = {'q': 'Kolomna', 'units': 'metric', 'lang': 'ru', 'appid': config.weather_apikey}
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)
            w = response.json()
            print(w)
            gradus_text = num2words(round(w['main']['temp']), lang='ru')
            gradus_int = int(round(w['main']['temp']))
            print(f"На улице {w['weather'][0]['description']} {gradus_text}")
            if gradus_int == 1 or gradus_int == -1 or gradus_int == 21 or gradus_int == -21:
                tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градус.")
            elif gradus_int in [2, 3, 4] or gradus_int in [-2, -3, -4, -22, -23, -24, -32, -33, -34]:
                tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градуса.")
            elif gradus_int >= 5 or gradus_int >= -5:
                if gradus_int in [22, 23, 24, 32, 33, 34] or gradus_int in [-22, -23, -24, -32, -33, -34]:
                    tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градуса.")
                else:
                    tts.va_speak(f"На улице, {w['weather'][0]['description']}, {gradus_text} градусов.")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Я бот.')
@bot.message_handler(func=lambda _: True)
def handle_message(message):
    time_start = datetime.now()
    # if message.from_user.username in config.users:
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.5,
        max_tokens=2000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0,
    )

    print('\n - user: ', message.from_user.username)
    print(' - question: ', message.text)
    print(' - response: ', response['choices'][0]['text'])
    time_end = datetime.now()
    time_request = time_end-time_start
    print(' - время запроса:', time_request)
    bot.send_message(chat_id=message.from_user.id, text=f"{response['choices'][0]['text']}")

# прослушивание
def polling():
    bot.send_message('1077463086', 'i`m online 🫡')
    try:
        bot.polling(none_stop=True)
    except:
        traceback_error_string = traceback.format_exc()
        # print('\r\n<<ERROR polling>>\r\n')
        print("\r\n\r\n" + time.strftime(
            "%c") + "\r\n<<ERROR polling>>\r\n" + traceback_error_string + "\r\n<<ERROR polling>>")
        with open(config.file_error_log, "a") as myfile:
            myfile.write("\r\n\r\n" + time.strftime(
                "%c") + "\r\n<<ERROR polling>>\r\n" + traceback_error_string + "\r\n<<ERROR polling>>")
            # myfile.write("\r\n --- error polling ---, " + time.strftime("%c") + "\n")
        bot.stop_polling()
        time.sleep(3)
        polling()
        bot.send_message('1077463086', f'{traceback.format_exc()}')
        bot.send_message('1077463086', 'ё-мае ... 😕')

if __name__ == '__main__':
    thread_tg = Thread(target=polling)
    thread_vosk = Thread(target=stt.va_listen, args=(va_respond,))
    thread_tg.start()
    thread_vosk.start()
