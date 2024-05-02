import os
from copy import copy
from .types import Mode
from .palette import Palette


# initialize real terminal
os.system("")


class Window:
    """
    Terminal window class
    """

    # terminal mode
    _mode: Mode | None = None

    # real terminal width and height
    _terminal_width: int = os.get_terminal_size().columns
    _terminal_height: int = os.get_terminal_size().lines

    # virtual terminal resolution (will equal to real one if high_res flag is not set)
    _width: int = _terminal_width
    _height: int = _terminal_height

    # terminal image buffer
    _disp_buffer: list[int] = list()

    # palette
    palette: list[int] = list()

    @property
    def mode(self):
        return self._mode

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def terminal_width(self):
        return self._terminal_width

    @property
    def terminal_height(self):
        return self._terminal_height

    @property
    def buffer(self):
        return self._disp_buffer

    @classmethod
    def initialize(cls, mode: Mode):
        """
        Initializes the window with given mode
        """

        # change mode
        cls._mode = mode

        # any kind of color mode cannot work with high_res flag
        if not mode & Mode.bw and mode & Mode.high_res:
            raise NotImplementedError("Unable to have color with high_res flag enabled")

        # update virtual width and height
        cls._width = cls._terminal_width if not mode & Mode.high_res else cls._terminal_width * 2
        cls._height = cls._terminal_height if not mode & Mode.high_res else cls._terminal_height * 4

        # initialize the image buffer
        cls._disp_buffer = [0 for _ in range(cls._width * cls._height)]

        # initialize palette
        if cls._mode & Mode.monochrome:
            cls.palette = copy(Palette.monochrome)
        elif cls._mode & Mode.palette4:
            cls.palette = copy(Palette.palette4)
        elif cls._mode & Mode.palette8:
            cls.palette = copy(Palette.palette8)
        else:  # full color or BW
            cls.palette = []

        # clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # make cursor invisible
        print('\33[?25l', end='', flush=True)

    @classmethod
    def plot(cls, x: int, y: int, val: int = 1):
        """
        Plots a value at given X and Y coord. Checks bounds.
        :param x: integer
        :param y: integer
        :param val: integer
        """

        if 0 < x < cls._width and 0 < y < cls._height:
            cls._disp_buffer[x + y * cls._width] = val

    @classmethod
    def copy_buffer(cls, buf: list[int]):
        """
        Copies given buffer into internal one. Size of buffer must equal to `width * height` (virtual width and height)
        :param buf: list of pixels, represented by integers. Order: left -> right; top -> bottom
        :raises IndexError: when buffer length is incorrect
        """

        # check buffer lengths
        if len(buf) != cls._width * cls._height:
            raise IndexError("Incorrect buffer length")

        cls._disp_buffer = copy(buf)

    @classmethod
    def clear(cls):
        """
        Clears internal image buffer
        """

        # easiest way is just to remake one
        cls._disp_buffer = [0 for _ in range(cls._width * cls._height)]

    @classmethod
    def update(cls):
        """
        Updates the image displayed
        """

        # printed string
        output = '\33[H'

        # update for BW terminal
        if cls._mode & Mode.bw:
            if not cls._mode & Mode.high_res:
                rows = [cls._disp_buffer[i*cls._width:i*cls._width+cls._width] for i in range(cls._height)]
                for row in rows:
                    output += ''.join(map(lambda x: ' ' if x == 0 else '#', row))
            else:
                p = lambda x: cls._disp_buffer[x]
                for yo in range(0, cls._height, 4):
                    for xo in range(0, cls._width, 2):
                        # calculate index
                        idx = xo + yo * cls._width

                        # first row
                        braille = p(idx)
                        braille += p(idx + 1) << 3

                        # second row
                        braille += p(idx + cls._width) << 1
                        braille += p(idx + 1 + cls._width) << 4

                        # third row
                        braille += p(idx + cls._width * 2) << 2
                        braille += p(idx + 1 + cls._width * 2) << 5

                        # forth row
                        braille += p(idx + cls._width * 3) << 6
                        braille += p(idx + 1 + cls._width * 3) << 7

                        output += chr(braille + 0x2800)
            print(output, end='', flush=True)
