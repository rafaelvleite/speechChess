#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 15:53:06 2020

@author: hack-rafa
"""

import speech_recognition as sr
from gtts import gTTS
import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import platform
import sys
import re    



##### CONFIGURAÇÕES #####
url = "https://www.chess.com/login_and_go?returnUrl=https%3A%2F%2Fwww.chess.com%2F"
user = "SEU_NOME_DE_USUARIO"
pwd = "SUA SENHA"

loginFieldType = "input"
loginFieldId = "username"

pwdFieldType = "password"
pwdFieldId = "password"


playUrl = "https://www.chess.com/analysis"


# AQUI VOCÊ DEVE COLOCAR O SEU JSON DE CREDENCIAL DO GOOGLE PARA A API GOOGLE SPEECH TO TEXT
with open('CAMINHO_DO_SEU_JSON') as credenciais_google:
    credenciais_google = credenciais_google.read()

executaAcao = False

hotword = 'fazer o lance'



# Navegador
options = Options()
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
options.add_argument('user-agent={0}'.format(user_agent))
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-infobars")
options.add_argument("start-maximized")
options.add_argument("--disable-extensions")
options.add_argument("--disable-single-click-autofill")
options.add_argument('log-level=1')

# Instalar extensão teclado no chess.com
# EXTENSÃO EM https://chrome.google.com/webstore/detail/chesscom-keyboard/bghaancnengidpcefpkbbppinjmfnlhh
# UTILIZEI ESTE SITE PARA BAIXAR O CRX DA A EXTENSÃO https://chrome-extension-downloader.com/
chrome_options = Options()
chrome_options.add_extension('./chrome_extensions/extension_5_4_0_0.crx')


# Pass the argument 1 to allow and 2 to block
options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 1
})

# Abrir browser
# AQUI VOCÊ PRECISA FAZER O DOWNLOAD DE UM DRIVER DE GOOGLE CHROME E ATUALIZAR O CAMINHO DO DRIVER
sistema_operacional = platform.platform().lower()
if "windows" in sistema_operacional:
    browser = webdriver.Chrome('./chrome_drivers/chromedriver_win32', options=options) 
elif "linux" in sistema_operacional:
    browser = webdriver.Chrome('./chrome_drivers/chromedriver_linux64', options=options) 
elif "mac" in sistema_operacional:
    browser = webdriver.Chrome('./chrome_drivers/chromedriver_mac64', options=options, chrome_options = chrome_options) 
elif "darwin" in sistema_operacional:
    browser = webdriver.Chrome('./chrome_drivers/chromedriver_mac64', options=options) 

# Ir para a página de login
browser.get(url)


# Aguardar carregamento completo da página
timeout = 15
element_present = EC.presence_of_element_located((By.ID, 'user-popover'))
WebDriverWait(browser, timeout).until(element_present)

# Preencher os campos de nome de usuário e senha
nameInputField = browser.find_element_by_id(loginFieldId)
nameInputField.send_keys(user)

pwdInputField = browser.find_element_by_id(pwdFieldId)
pwdInputField.send_keys(pwd)

submitButton = browser.find_element_by_xpath("//button[@type='submit' and @name='login']")
submitButton.click()


# Aguardar carregamento completo da página
timeout = 15
element_present = EC.presence_of_element_located((By.ID, 'cdm-zone-end'))
WebDriverWait(browser, timeout).until(element_present)


# Ir para a página de jogar
browser.get(playUrl)


# Aguardar carregamento completo da página
timeout = 15
element_present = EC.presence_of_element_located((By.ID, 'board-layout-main'))
WebDriverWait(browser, timeout).until(element_present)


def transformarLance(lance):
    lanceTransformado = lance.lower()
    lanceTransformado = lanceTransformado.replace("de ", "d")
    lanceTransformado = lanceTransformado.replace("se ", "c")
    lanceTransformado = lanceTransformado.replace("um", "1")
    lanceTransformado = lanceTransformado.replace("dois", "2")
    lanceTransformado = lanceTransformado.replace("três", "3")
    lanceTransformado = lanceTransformado.replace("quatro", "4")
    lanceTransformado = lanceTransformado.replace("cinco", "5")
    lanceTransformado = lanceTransformado.replace("seis", "6")
    lanceTransformado = lanceTransformado.replace("sete", "7")
    lanceTransformado = lanceTransformado.replace("oito", "8")
    lanceTransformado = lanceTransformado.replace("cavalo", "N")
    lanceTransformado = lanceTransformado.replace("rei", "K")
    lanceTransformado = lanceTransformado.replace("torre", "R")
    lanceTransformado = lanceTransformado.replace("dama", "Q")
    lanceTransformado = lanceTransformado.replace("rainha", "Q")
    lanceTransformado = lanceTransformado.replace("bispo", "B")
    lanceTransformado = lanceTransformado.replace("rock", "roque")
    lanceTransformado = lanceTransformado.replace("grande roque", "000")
    lanceTransformado = lanceTransformado.replace("longo roque", "000")
    lanceTransformado = lanceTransformado.replace("roque grande", "000")
    lanceTransformado = lanceTransformado.replace("roque longo", "000")
    lanceTransformado = lanceTransformado.replace("pequeno roque", "00")
    lanceTransformado = lanceTransformado.replace("roque pequeno", "00")
    lanceTransformado = lanceTransformado.replace("roque curto", "00")
    lanceTransformado = lanceTransformado.replace("roque", "00")
    lanceTransformado = lanceTransformado.replace(" por ", "x")
    lanceTransformado = lanceTransformado.replace("por", "x")
    lanceTransformado = lanceTransformado.strip()
    lanceTransformado = re.sub(' ','',lanceTransformado)
    if (lanceTransformado[-2] == '8') or (lanceTransformado[-2] == '1'): 
        lanceTransformado = lanceTransformado[:-1] + '=' + lanceTransformado[-1]
    
    return lanceTransformado


def fazerLance(browser, lance):
    helperField = browser.find_elements_by_class_name("ccHelper-input")[0]
    helperField.click()
    helperField.clear()
    helperField.click()
    helperField.send_keys(lance)
    helperField.send_keys(Keys.ENTER)
    

def setStatusTrigger(status):
    global executaAcao
    executaAcao = status

def getStatusTrigger():
    return executaAcao

def analisarAcao(comando, hotword, browser):
    if "navegador" in comando:
        responder('tchau')
        browser.quit()
        sys.exit()
    if hotword in comando:
        retornarLanceEmTexto(comando, hotword, browser)
    

def retornarLanceEmTexto(comando, hotword, browser):
    lance = comando.split(hotword)[1][1:]
    print(lance)
    criarAudio(lance, 'lance')
    responder('lance')
    lance = transformarLance(lance)
    fazerLance(browser, lance)
    

def criarAudio(texto, nome_arquivo):
    tts = gTTS(texto, lang='pt-br')
    path = './audios/' + nome_arquivo + '.mp3'
    with open(path, 'wb') as file:
        tts.write_to_fp(file)

def responder(nome_arquivo):
    path = 'audios/' + nome_arquivo + '.mp3'
    subprocess.call(["afplay", path])
    
    

def monitorarAudio(hotword):
    microfone = sr.Recognizer()
    
    with sr.Microphone() as source:
        responder('beep_01')
        print("Aguardando o Comando: ")
        audio = microfone.listen(source)
        

    try:
        trigger = microfone.recognize_google_cloud(audio, credentials_json=credenciais_google, language='pt-BR')
        #trigger = microfone.recognize_google(audio,language='pt-BR')
        trigger = trigger.lower()
        print(trigger)
        if trigger.strip() == hotword.strip():
            return None
        if hotword in trigger and not getStatusTrigger():
            print('Comando reconhecido!')
            setStatusTrigger(True)
        elif getStatusTrigger():
            setStatusTrigger(False)
        return trigger
    except sr.UnknownValueError:
        print("Google not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Cloud Speech service; {0}".format(e))

    return None


criarAudio('Até logo!', 'tchau')


while True:
    comando = monitorarAudio(hotword)
    if comando is not None:
        print(comando)
        analisarAcao(comando, hotword, browser)


#browser.quit()







