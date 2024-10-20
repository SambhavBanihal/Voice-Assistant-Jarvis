import pyttsx3
import time
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import subprocess
import openai

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

# Select a voice that might be clearer (voice[0] or voice[1], depending on your system)
engine.setProperty('voice', voices[0].id)  # Try [1] if this isn't clear
engine.setProperty('rate', 150)  # Adjust rate for better pronunciation
engine.setProperty('volume', 1.0)  # Ensure volume is at max

# OpenAI API key setup
openai.api_key = 'your_openai_api_key_here'

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning Mister Sambhav, I am Jarvis!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon Mister Sambhav, I am Jarvis!")
    else:
        speak("Good Evening Mister Sambhav, I am Jarvis!")
    
    time.sleep(1)    
    speak(" !!   HELLO BOSS! How can I assist you?")

def takecommand():
    '''Microphone input, string output'''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..........")
        r.pause_threshold = 1
        audio = r.listen(source)
        
        try:
            print("Recognizing........")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Say it again please")
            return "None"
        
        return query

def send_email(to_address, subject, body):
    '''Send an email'''
    from_address = 'your_email@example.com'  # Replace with your email address
    password = 'your_password'  # Replace with your email password
    
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.example.com', 587)  # Replace with your SMTP server and port
        server.starttls()
        server.login(from_address, password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        speak("Sorry, I was unable to send the email.")
        print(f"Error: {e}")

def open_application(name):
    '''Open an application by its name'''
    apps = {
        'visual studio code': r"C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
        'chrome': r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        'firefox': r"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
        'notepad': r"C:\\Windows\\System32\\notepad.exe"
        # Add more applications here
    }
    
    path = apps.get(name.lower())
    if path:
        if os.path.exists(path):
            os.startfile(path)
            speak(f"Opening {name}")
        else:
            speak("Application not found.")
    else:
        speak("Application not recognized.")

def shutdown_pc():
    '''Shutdown the PC'''
    speak("Shutting down the PC")
    subprocess.run(["shutdown", "/s", "/t", "0"])

def chat_with_gpt(prompt):
    '''Interact with OpenAI's GPT model using the new API'''
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use the model you prefer (gpt-3.5-turbo or gpt-4)
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't get a response from ChatGPT."

if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand().lower()  # Always convert the input to lowercase for consistency
        
        if 'wikipedia' in query:
            speak('Searching Wikipedia')
            query = query.replace(" according to wikipedia", "")
            results = wikipedia.summary(query, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        
        elif 'open youtube' in query:
            speak("As you wish my lord, opening YouTube")
            webbrowser.open("https://www.youtube.com")
            
        elif 'open google' in query:
            speak("As you wish my lord, opening Google")
            webbrowser.open("https://www.google.com")

        elif 'play music' in query:
            music_path = r"C:\\Users\\HP\\Music\\We don't Talk Anymore.mp3"  
            speak("Playing music")
            os.endfile(music_path)  
            
            
        elif 'play music' in query:
            music_path = r"C:\\Users\\HP\\Music\\We don't Talk Anymore.mp3"  
            speak("Playing music")
            os.startfile(music_path)
            
        elif 'open code' in query:
            cpath = r"C:\\Users\\HP\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"  # Path to VS Code executable
            speak("Opening Visual Studio Code")
            os.startfile(cpath)  # Opens the actual executable file
        
        elif 'what is the time' in query or 'what\'s the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif 'send email' in query:
            speak("Sure, to whom should I send the email?")
            to_address = takecommand()  # Get recipient email address
            
            speak("What should be the subject of the email?")
            subject = takecommand()  # Get subject
            
            speak("What should be the body of the email?")
            body = takecommand()  # Get email body
            
            # Sending email
            send_email(to_address, subject, body)

        elif 'open' in query:
            app_name = query.replace('open', '').strip()
            open_application(app_name)
            
        elif 'shut down' in query:
            shutdown_pc()

        elif 'chat' in query:
            prompt = query.replace('chat', '').strip()
            response = chat_with_gpt(prompt)
            speak(response)
            print(response)
