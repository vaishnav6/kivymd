from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
import speech_recognition as sr
import pyttsx3
from datetime import *

class Vimoweb(MDApp):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(Builder.load_file("intro.kv"))
        self.sm.add_widget(Builder.load_file("home.kv"))
        return self.sm
    
    def on_start(self):
        Clock.schedule_once(self.change_screen, 2)
        Clock.schedule_interval(self.update_time, 1)  # Update time every second

    def change_screen(self, dt):
        self.sm.current = "Home"
    
    def speak(self, txt):  # Added self argument
        engine = pyttsx3.init()
        engine.say(txt)
        engine.runAndWait()

    def update_time(self, dt):  # Function to update time
        today = date.today()
        cdate = today.strftime("%d/%m/%Y")
        ctime = datetime.now().time()
        hour = ctime.hour
        minute = ctime.minute
        dtcondition = "PM" if hour >= 12 else "AM"
        hour = hour if hour <= 12 else hour - 12 if hour != 0 else 12  # Convert hour to 12-hour format
        self.sm.get_screen("Home").ids.times.text = f"Time: {hour:02d}:{minute:02d} {dtcondition}"
        self.sm.get_screen("Home").ids.dates.text = f"Date: {cdate}"

    def recognize(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something :")
            recognizer.adjust_for_ambient_noise(source, duration=0.1)
            try:
                audio = recognizer.listen(source)
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                if "hello" in text.lower():
                    self.speak("Hello Sir What Can I Do For You")
                    self.sm.get_screen("Home").ids.reply.text = "Hello Sir What Can I Do For You"
                else:
                    self.speak("Could Not Understand Try Again")
                    self.sm.get_screen("Home").ids.reply.text = "Try Again"
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Error making a request to Google Speech Recognition service: {e}")

Vimoweb().run()
