from tty import setraw
from termios import tcgetattr, tcsetattr, TCSAFLUSH
from threading import Thread
from os import read, write
from sys import stdin, exit
from signal import signal, SIGTERM, SIGINT, SIGHUP

from .websocket import Websocket, WebsocketError


class RawTerminal:
    def __init__(self, websocket_url):
        self.fd = stdin.fileno()
        self.websocket = Websocket(websocket_url)

        self.writer_thread = None


    def make_raw(self):
        self.terminal_attrs = tcgetattr(self.fd)
        setraw(self.fd)


    def restore_terminal(self):
        tcsetattr(self.fd, TCSAFLUSH, self.terminal_attrs)


    def run(self):
        self.websocket.connect()

        for signum in (SIGTERM, SIGINT, SIGHUP):
            signal(signum, self.exit)

        self.make_raw()

        self.writer_thread = Thread(
            target = self.writer, daemon = True
        )
        self.writer_thread.start()

        self.reader()

        self.exit()


    def exit(self, signum = None, frame = None):
        self.restore_terminal()

        print('')

        exit(0)


    def reader(self):
        while True:
            try:
                data = self.websocket.read()
            except WebsocketError:
                break

            if data is not None:
                write(self.fd, data)


    def writer(self):
        while True:
            data = read(self.fd, 4096)

            if not data:
                break

            try:
                self.websocket.write(data)
            except WebsocketError:
                break

