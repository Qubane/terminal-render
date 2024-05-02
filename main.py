from src import *
from time import sleep


def main():
    win = Window()
    win.initialize(Mode.bw)
    count = 0
    while True:
        win.update()
        win._disp_buffer[count-1] = 0
        win._disp_buffer[count] = 1
        count = (count + 1) % 3600
        # sleep(0.0333)  # ~1/30


if __name__ == '__main__':
    main()
