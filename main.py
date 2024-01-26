from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
import speech_recognition as sr
import pyttsx3
import webbrowser
from threading import Thread
from kivy.clock import Clock

class VoiceAssistantApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 200)
        self.is_listening = False

    def build(self):
        self.title = "Voice Assistant"
        self.root_layout = BoxLayout(orientation='vertical')
        
        self.label = MDLabel(
            text="VIMO ASSISTANT",
            halign="center"
        )
        
        self.start_button = MDRaisedButton(
            text="Start Assistant",
            halign="center",
            on_release=self.start_listening
        )

        self.root_layout.add_widget(self.label)
        self.root_layout.add_widget(self.start_button)

        return self.root_layout

    def speak(self, audio):
        self.engine.say(audio)
        self.engine.runAndWait()

    def start_listening(self, *args):
        self.is_listening = True
        Thread(target=self.listen_for_commands).start()

    def listen_for_commands(self):
        with sr.Microphone() as source:
            print("Listening...")
            while self.is_listening:
                self.recognizer.adjust_for_ambient_noise(source)
                audio = self.recognizer.listen(source)
                try:
                    text = self.recognizer.recognize_google(audio)
                    print("Command : ", text)
                    Clock.schedule_once(lambda dt: self.handle_command(text.lower()))
                except sr.UnknownValueError:
                    print("Sorry, could not understand audio.")
                except sr.RequestError as e:
                    print("Error: {0}".format(e))

    def handle_command(self, command):
        if "hello" in command:
            self.speak("Hello! I am here to assist you.")
        elif "how are you" in command:
            self.speak("I am fine. What about you?")
        elif "open youtube" in command:
            self.speak("What do you want to search?")
            search_query = self.listen()
            if search_query:
                url = "https://www.youtube.com/results?search_query=" + search_query
                webbrowser.open(url)
        elif "open chrome" in command:
            self.speak("What do you want to search?")
            search_query = self.listen()
            if search_query:
                url = "https://www.google.com/search?q=" + search_query
                webbrowser.open(url)
        elif "stop" in command:
            self.speak("Goodbye! Have a nice day.")
            self.is_listening = False
        else:
            self.speak("Sorry, I didn't understand that command.")

    def listen(self):
        with sr.Microphone() as source:
            print("Listening for search query...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)
        try:
            text = self.recognizer.recognize_google(audio)
            print("Search Query : ", text)
            return text.lower()
        except sr.UnknownValueError:
            print("Sorry, could not understand search query.")
            return ""
        except sr.RequestError as e:
            print("Error: {0}".format(e))
            return ""

if __name__ == "__main__":
    VoiceAssistantApp().run()
