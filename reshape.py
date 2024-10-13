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
        """
        Open a file chooser dialog for selecting image files.

        This method launches a file chooser dialog that allows the user to select
        either JPEG (.jpg) or PNG (.png) image files. Once a file is selected,
        the 'selected' method of this class will be called with the chosen file(s).

        The file chooser is configured with the following filters:
        - JPEG Files (*.jpg)
        - PNG Files (*.png)
        """
        filechooser.open_file(on_selection=self.selected, filters=[("JPEG Files", "*.jpg"),("PNG Files", "*.png")])

    def selected(self, selection):
        """
        Process the selected image file.

        This method is called when a file is selected from the file chooser.
        It performs the following operations:
        1. Stores the original file path.
        2. Opens the selected image.
        3. Resizes the image to 680x453 pixels using LANCZOS resampling.
        4. Saves the resized image as a preview.
        5. Updates the image source for display.

        Args:
            selection: A list containing the path of the selected file.
                while a list is possible as user can select multiple files only the first file is used
        """
        if selection:
            self.original_path = selection[0]
            with Image.open(selection[0]) as img:
                resized = img.resize((680, 453), Image.Resampling.LANCZOS)
                preview_path = 'preview.png'
                resized.save(preview_path)
                self.image_source = preview_path

    def resize_image(self):
        """
        Resize the original image and update the display.

        This method performs the following operations:
        1. Checks if an original image path exists.
        2. Opens the original image.
        3. Resizes the image to 680x453 pixels using LANCZOS resampling.
        4. Saves the resized image, overwriting the original file.
        5. Updates the image_source to display the resized image.
        6. Removes the temporary preview image if it exists.

        The method only executes if an original image path has been set.
        After resizing, the original file is replaced with the resized version.
        The temporary 'preview.png' file is deleted to clean up resources.
        """
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
