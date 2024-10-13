import kivy
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.animation import Animation
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from PIL import Image
from plyer import filechooser
from gradient import gradient
from itertools import chain
from kivy.graphics.texture import Texture
import numpy as np

from kivy.lang import Builder
Builder.load_string("""
#:import gradient gradient.gradient
""")

kivy.require('2.3.0')

class MyRoot(BoxLayout):
    """functions go here """
    image_source = StringProperty("")

    def __init__(self):
        super(MyRoot, self).__init__()

    def choose_file(self):
        filechooser.open_file(on_selection=self.selected, filters=[("JPEG Files", "*.jpg"),("PNG Files", "*.png")])

    def selected(self, selection):
        if selection:
            self.original_path = selection[0]
            with Image.open(selection[0]) as img:
                resized = img.resize((680, 453), Image.Resampling.LANCZOS)
                preview_path = 'preview.png'
                resized.save(preview_path)
                self.image_source = preview_path

    def resize_image(self):
        if hasattr(self, 'original_path'):
            with Image.open(self.original_path) as img:
                resized = img.resize((680, 453), Image.Resampling.LANCZOS)
                resized.save(self.original_path)
            self.image_source = self.original_path

            if os.path.exists('preview.png'):
                os.remove('preview.png')


class resize(App):
    """app gets build here"""
    def build(self):
        return MyRoot()

if __name__ == "__main__":
    rz_image  = resize()
    Window.size = (800, 650)
    rz_image.run()
