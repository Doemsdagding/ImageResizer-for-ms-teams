from itertools import chain
from kivy.graphics.texture import Texture
import numpy as np

class gradient(object):

    @staticmethod
    def diagonal(*args):
        """
        Create a diagonal gradient texture.

        This method generates a square texture with a diagonal gradient using the provided color arguments.
        The gradient transitions smoothly between the given colors along the diagonal.

        Args:
            *args: Variable number of color tuples. Each tuple should contain 4 float values (r, g, b, a)
               representing red, green, blue, and alpha channels respectively, each in the range [0, 1].

        Returns:
            Texture: A Kivy Texture object representing the diagonal gradient.

        The size of the texture is determined by the number of color arguments provided.
        The gradient is created using NumPy for efficient computation.
        """
        size = len(args)
        texture = Texture.create(size=(size, size), colorfmt='rgba')

        # Create a diagonal gradient using numpy
        gradient = np.zeros((size, size, 4), dtype=np.uint8)
        for i in range(size):
            for j in range(size):
                t = (i + j) / (2 * size - 2)
                color = np.array(args[int(t * (len(args) - 1))])
                gradient[i, j] = (color * 255).astype(np.uint8)

        # Convert the numpy array to bytes
        buf = gradient.tobytes()

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture
