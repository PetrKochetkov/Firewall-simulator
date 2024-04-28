import os
import signal
import keyboard
import multiprocessing
import sys


def hook(pid):
    while True:
        if keyboard.is_pressed('ctrl + h'):
            os.kill(pid, signal.SIGTERM)
            sys.exit(1)


if __name__ == '__main__':
    pid = os.getpid()
    multiprocessing.Process(target=hook, args=[pid]).start()
    while True:
        print('fdfdfsfs')
