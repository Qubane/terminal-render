from enum import Flag, auto


class Mode(Flag):
    """
    Mode enum class
    """

    bw = auto()             # black and white
    monochrome = auto()     # monochrome (2 colors)
    palette4 = auto()       # palette (16 colors)
    palette8 = auto()       # palette (256 colors)
    rgb = auto()            # full rgb

    high_res = auto()       # use braille unicode characters
