from itertools import chain
from kivy.graphics.texture import Texture
import numpy as np

class gradient(object):

    @staticmethod
    def diagonal(*args):
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