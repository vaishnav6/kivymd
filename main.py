from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

import requests

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTextField:
        id: number_input
        hint_text: "Enter number"
        helper_text: "Enter the number you want to search"
        helper_text_mode: "on_focus"

    MDRaisedButton:
        text: "Search"
        on_release: app.search_number()
        
    MDTextField:
        id: output_text
        hint_text: "Output"
        readonly: True
'''

class MyApp(App):
    def build(self):
        return Builder.load_string(KV)

    def search_number(self):
        number_input = self.root.ids.number_input.text
        output_text = self.root.ids.output_text

        url = "https://callapp.p.rapidapi.com/api/v1/search"
        querystring = {"code": "91", "number": number_input}
        headers = {
            "X-RapidAPI-Key": "ef2f84ab76msh987eb43930116fep1b2080jsn6a5f354fcc03",
            "X-RapidAPI-Host": "callapp.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        if response.status_code == 200:
            output_text.text = str(response.json())
        else:
            output_text.text = "Error: Unable to fetch data"


if __name__ == '__main__':
    MyApp().run()
