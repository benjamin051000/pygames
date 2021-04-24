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
