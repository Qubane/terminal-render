import math
from src import *
from time import sleep


def main():
    win = Window()
    # win.initialize(Mode.bw | Mode.high_res)
    win.initialize(Mode.bw)

    count = 0
    while True:
        win.update()
        win.clear()
        for i in range(win.width):
            val = (math.sin(i / 20 + (count / 10)) + 1) / 2
            y = int(val * win.height * 0.8) + 1
            win.plot(i, y)
        # win.buffer[(count-1) % len(win.buffer)] = 0
        # win.buffer[count % len(win.buffer)] = 1
        count += 1
        sleep(0.0333)  # ~1/30


if __name__ == '__main__':
    main()
