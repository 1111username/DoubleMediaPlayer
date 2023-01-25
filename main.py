from sys import argv

from globalvar.globalvars import GlobalVars
from window.mainwindow import BaseWindow


def log(tag: str, message: str):
    print(f"{tag} - {message}")


def print_message(message: bytes):
    print(message)


if __name__ == '__main__':
    if len(argv) == 3 and argv[1] == '-port':
        GlobalVars.myPort = int(argv[2])
    program = BaseWindow()
    program.start()
