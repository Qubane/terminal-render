import math
from time import sleep
from TerminalRender import *


def main():
    win = Window()
    win.initialize(Mode.rgb)

    count = 0
    while True:
        win.update()
        win.clear()
        for i in range(win.width):
            val = (math.sin(i / 20 + (count / 10)) + 1) / 2
            y = int(val * win.height * 0.8) + 1
            win.plot(i, y, int(val * 255) << 8)
        count += 1
        sleep(0.0333)  # ~1/30


if __name__ == '__main__':
    main()
