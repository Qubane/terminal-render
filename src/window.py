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

    @classmethod
    def initialize(cls, mode: Mode):
        """
        Initializes the window with given mode
        """

        # change mode
        cls._mode = mode

        # any kind of color mode cannot work with high_res flag
        if mode is not Mode.bw and mode is Mode.high_res:
            raise NotImplementedError("Unable to have color with high_res flag enabled")

        # update virtual width and height
        cls._width = cls._terminal_width if mode is not Mode.high_res else cls._terminal_width * 2
        cls._height = cls._terminal_height if mode is not Mode.high_res else cls._terminal_height * 4

        # initialize the image buffer
        cls._disp_buffer = [0 for _ in range(cls._width * cls._height)]

        # initialize palette
        if cls._mode is Mode.monochrome:
            cls.palette = copy(Palette.monochrome)
        elif cls._mode is Mode.palette4:
            cls.palette = copy(Palette.palette4)
        elif cls._mode is Mode.palette8:
            cls.palette = copy(Palette.palette8)
        else:  # full color or BW
            cls.palette = []

        # clear the terminal
        os.system('cls' if os.name == 'nt' else 'clear')

        # make cursor invisible
        print('\33[?25l', end='', flush=True)

    @classmethod
    def update(cls):
        """
        Updates the image displayed
        """

        # printed string
        output = '\33[H'

        # update for BW terminal
        if cls._mode is Mode.bw:
            rows = [cls._disp_buffer[i*cls._width:i*cls._width+cls._width] for i in range(cls._height)]
            for row in rows:
                output += ''.join(map(lambda x: ' ' if x == 0 else '#', row))
            print(output, end='', flush=True)
