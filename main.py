from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

kv = """
MDFloatLayout:
    md_bg_color: "black"
    Image:
        source: 'lion.png'
        size_hint: None, None
        size: 300, 300
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
    Label:
        id: typing
        text: ""
        color: "gold"
        font_size: 25
        bold: True
        pos_hint: {"center_x": 0.5,"center_y": 0.29}
        
"""

class Vimoweb(MDApp):
    current_index = 0
    text_to_type = "VIMOWEB"

    def build(self):
        return Builder.load_string(kv)
    
    def typing(self, *args):
        if self.current_index < len(self.text_to_type):
            current_index = self.root.ids.typing.text
            current_index += self.text_to_type[self.current_index]
            self.root.ids.typing.text = current_index
            self.current_index += 1
        else:
            Clock.unschedule(self.typing)
        
    def on_start(self):
        Clock.schedule_interval(self.typing, 0.1)

if __name__ == '__main__':
    Vimoweb().run()
