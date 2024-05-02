from src import *
from time import sleep


def main():
    win = Window()
    win.initialize(Mode.bw)
    count = 0
    while True:
        win.update()
        for i in range(3600):
            win._disp_buffer[i] = (i + count + (i // 120)) % 6
        count += 1
        # sleep(0.0333)  # ~1/30


if __name__ == '__main__':
    main()
