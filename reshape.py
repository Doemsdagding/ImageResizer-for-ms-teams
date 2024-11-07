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
from gradient import gradient
from itertools import chain
from kivy.graphics.texture import Texture
import numpy as np

from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup

from kivy.lang import Builder
Builder.load_string("""
#:import gradient gradient.gradient
""")

kivy.require("2.3.0")

class MyRoot(BoxLayout):
    """functions go here """
    image_source = StringProperty("")

    def __init__(self):
        super(MyRoot, self).__init__()

    def choose_file(self):
        """
            *opens a file selector window
            *execute the selected function
        """
        default_path = os.path.join(os.path.expanduser("~"), "C:\\Users\\gold-\\AppData\\Roaming\\Microsoft\\Teams\\Backgrounds\\Uploads")
        # Use default path if exists, otherwise fallback to home directory
        start_path = default_path if os.path.exists(default_path) else os.path.expanduser("~")

        content = BoxLayout(orientation="vertical")
        file_chooser = FileChooserIconView(
            filters=["*.jpg", "*.png"],
            path=start_path
        )

        def select_file(instance):
            if file_chooser.selection:
                self.selected(file_chooser.selection)
                popup.dismiss()

        # Create buttons for the popup
        buttons = BoxLayout(size_hint_y=None, height=40)
        select_button = Button(text="Select", size_hint_x=0.5)
        cancel_button = Button(text="Cancel", size_hint_x=0.5)

        select_button.bind(on_release=select_file)
        cancel_button.bind(on_release=lambda x: popup.dismiss())

        buttons.add_widget(select_button)
        buttons.add_widget(cancel_button)

        content.add_widget(file_chooser)
        content.add_widget(buttons)

        popup = Popup(
            title="Choose an image file",
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()

    def selected(self, selection):
        """
        *Process the selected image file.
        *Update the image path and preview.

        Args:
            selection: A list containing the path of the selected file.
                while a list is possible as user can select multiple files only the first file is used
        """
        if selection:
            self.original_path = selection[0]
            self.ids.image_path.text = selection[0]
            with Image.open(selection[0]) as img:
                resized = img.resize((680, 453), Image.Resampling.LANCZOS)
                preview_path = "preview.png"
                resized.save(preview_path)
                self.image_source = preview_path

    def resize_image(self):
        """
        Resize the original image and update the display.

        The method only executes if an original image path has been set.
        After resizing, the original file is replaced with the resized version.
        The temporary "preview.png" file is deleted to clean up resources.
        """
        if hasattr(self, "original_path"):
            with Image.open(self.original_path) as img:
                resized = img.resize((680, 453), Image.Resampling.LANCZOS)
                resized.save(self.original_path)
            self.image_source = self.original_path

            if os.path.exists("preview.png"):
                os.remove("preview.png")


class resize(App):
    """app gets build here"""
    def build(self):
        return MyRoot()

if __name__ == "__main__":
    rz_image  = resize()
    Window.size = (800, 650)
    rz_image.run()
