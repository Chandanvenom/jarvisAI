import random

import speech_recognition as sr
import webbrowser
import win32com.client
import os
import datetime
import pyautogui
import openai
from config import apikey
import requests
from bs4 import BeautifulSoup
speaker = win32com.client.Dispatch("SAPI.SpVoice")
chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Chandan: {query}\n Jarvis: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    speaker.Speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]



def ai(prompt):
    openai.api_key = apikey
    text =f"OpenAI response for Promt: {prompt} \n ********************\n\n"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    print(response['choices'][0]['text'])
    text +=response['choices'][0]['text']
    if not os.path.exists("Openai"):
        os.mkdir("Openai")
    with open(f"Openai/{' '.join(prompt.split('intelligence')[1:])}","w") as  f:
        f.write(text)

def take():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some error occurred. Sorry from jarvis"


# class Amay:
#     pass


if __name__ == '__main__':
     speaker.Speak("helllo i am jarvis AI ")
     while True:

         print("listening...")
         query = take()
         sites=[["youtube","https://www.youtube.com"],["wikipedia","https://www.wikipedia.com"],["google","https://www.google.com"]]
         for site in sites:
             if f"open {site[0]}".lower() in query.lower():
                 speaker.Speak(f"Opening {site[0]} sir ..")
                 webbrowser.open(site[1])
         if "play music" in query:
             music = "D:\Music"
             songs = os.listdir(music)
             os.startfile(os.path.join(music , songs[1]))
         elif "the time" in query:
             strfTime = datetime.datetime.now().strftime("%H:%M:%S")
             speaker.Speak(f"Sir the time is {strfTime}")
         elif "open" in query:
             query=query.replace("open","")
             query=query.replace("jarvis","")
             pyautogui.press("super")
             pyautogui.typewrite(query)
             pyautogui.sleep(2)
             pyautogui.press("enter")
         elif "using artificial intelligence".lower() in query.lower():
             ai(prompt=query)
         elif "quit".lower() in query.lower():
             exit()
         elif "reset chat".lower() in query.lower():
             chatStr=""
         elif "temperature".lower() in query.lower():
             search="Temperature in Kolkata"
             url=f"https://www.google.com/search?q={search}"
             r=requests.get(url)
             data=BeautifulSoup(r.text,"html.parser")
             temp=data.find("div",class_="BNeawe").text
             speaker.Speak(f"current {search} in {temp}")

         else:
             print("chatting...")
             chat(query)




         # if "open music" in query:
         #    import playsound
         #    playsound("C:\Users\cnask\Desktop\py\song")
         # # speaker.Speak(query)



