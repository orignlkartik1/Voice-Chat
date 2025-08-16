import os
import speech_recognition as sr
import pyttsx3 as py
import datetime as dt
import wikipedia as wiki
import webbrowser as wb
import pyjokes as pj

import google.generativeai as gen

gen.configure(api_key="You-api")

def gemini_reply(prompt):
    model = gen.GenerativeModel("gemini-1.5-flash")  # Fast & free
    response = model.generate_content(prompt)
    return response.text

### If you wanna integrate OpenAI you can use this

#from openai import OpenAI
#client=OpenAI(api_key=("Your_OPen_Ai_Key"))

# def chatgpt_reply(prompt):
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o-mini",  # You can change to gpt-4 or gpt-3.5
#             messages=[
#                 {"role": "system", "content": "You are a helpful AI assistant."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
#         return response.choices[0].message.content
#     except Exception as e:
#         return f"Error: {e}"

def speak(text):
    print(f"Assistant: {text}")
    try:
        engine = py.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(text)
        engine.runAndWait()
    except:
        print("Speech output not supported in Colab.")


def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio).lower()
            #print(r.recognize_google(audio).lower())
        except:
            return "Sorry, I didn't catch that."

def greet():
    hour = int(dt.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your voice assistant . How can I help you today?")

# def take():
#     return input("You (type your command): ").lower()

def write_query(query):
    print(f"User query : {query}")

def run():
    greet()
    while True:
        query = listen()
        write_query(query)

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            try:
                result = wiki.summary(query, sentences=2)
                speak("According to Wikipedia:")
                speak(result)
            except:
                speak("Sorry, I couldn't find anything.")

        elif "notepad" in query:
            os.system("notepad")

        elif "calculator" in query:
            os.system("calc")

        elif 'open youtube' in query:
            speak("Opening YouTube...")
            wb.open("https://www.youtube.com/")

        elif 'open google' in query:
            speak("Opening Google...")
            wb.open("https://www.google.com/")

        elif 'time' in query:
            strTime = dt.datetime.now().strftime("%H:%M:%S")
            speak(f"The current time is {strTime}")

        elif 'joke' in query:
            joke = pj.get_joke()
            speak(joke)

        elif "learn" in query:
            speak("learn anything.......")
            wb.open('https://learn-anything.xyz/')

        elif 'exit' in query or 'bye' in query:
            speak("Goodbye! Have a nice day!")
            break

        else:
            speak("Let me think...")
            # answer = chatgpt_reply(query)
            answer=gemini_reply(query)
            speak(answer)
run()
