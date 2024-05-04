class Palette:
    """
    ANSI escape codes for colors
    """

    monochrome: list[int] = [
        '\33[30m',      # black
        '\33[37m'       # white
    ]

    palette4: list[int] = [
        '\33[30m',      # black
        '\33[90m',      # bright black
        '\33[31m',      # red
        '\33[91m',      # bright red
        '\33[32m',      # green
        '\33[92m',      # bright green
        '\33[33m',      # yellow
        '\33[93m',      # bright yellow
        '\33[34m',      # blue
        '\33[94m',      # bright blue
        '\33[35m',      # magenta
        '\33[95m',      # bright magenta
        '\33[36m',      # cyan
        '\33[96m',      # bright cyan
        '\33[37m',      # white
        '\33[97m'       # bright white
    ]

    palette8: list[int] = [
        f'\33[38;5;{i}m' for i in range(256)
    ]
