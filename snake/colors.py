"""
colors.py
Contains R,G,B color constants.

"""
from enum import Enum

class Colors(Enum):
    """ Color Constants. Format: (R, G, B). """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)

    def __add__(self, other):
        return (self.value[0] + other[0], self.value[1] + other[1], self.value[2] + other[2])
