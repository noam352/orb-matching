import enum
import random


class Color(enum.Enum):
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)
    Yellow = (255, 255, 0)
    Purple = (127, 0, 255)
    Black = (30, 30, 30)
    # transparent = (255, 0, 0, 128)
    white = (255, 255, 255)

    @staticmethod
    def random():
        return list(Color)[random.randint(0, len(Color) - 3)]
