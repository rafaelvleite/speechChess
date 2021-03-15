#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 15 15:06:36 2021

@author: hack-rafa
"""
# referências
# https://towardsdatascience.com/how-to-build-your-own-ai-personal-assistant-using-python-f57247b4494b
# https://github.com/mmirthula02/AI-Personal-Voice-assistant-using-Python/blob/master/venv/virtual.py


import speech_recognition as sr
import pyttsx3
import datetime
import time
import subprocess
import platform



print('Carregando o seu assistente virtual - Freedom Chess')

if 'Darwin' in platform.system():
    engine=pyttsx3.init('nsss')
elif 'Windows' in platform.system():
    engine=pyttsx3.init('sapi5')
voices=engine.getProperty('voices')
engine.setProperty('voice','voices[0].id')


def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Olá, bom dia")
        print("Olá, bom dia")
    elif hour>=12 and hour<18:
        speak("Olá, boa tarde")
        print("Olá, boa tarde")
    else:
        speak("Olá, boa noite")
        print("Olá, boa noite")

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Ouvindo...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='pt-BR')
            print(f"usuário disse:{statement}\n")

        except Exception as e:
            print("Vamos para mais um loop")
            return "None"
        return statement

speak("Carregando o seu assistente virtual - Freedom Chess")
wishMe()


if __name__=='__main__':


    while True:
        #speak("Tell me how can I help you now?")
        statement = takeCommand().lower()
        if statement==0:
            continue

        if "lance" in statement:
            speak("Vamos fazer o lance")
            print('Vamos fazer o lance')


        elif "sair" in statement:
            speak("Tudo bem , vamos encerrar")
            subprocess.call(["shutdown", "/l"])
            break



