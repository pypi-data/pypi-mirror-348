import threading
import signal

from socketserver import ThreadingTCPServer, BaseRequestHandler
from socket import AF_INET6
from time import sleep
from os import _exit as exit
from subprocess import Popen

from .websocket import Websocket, WebsocketError
from .errors import SystemError


class TCPServer(ThreadingTCPServer):
    allow_reuse_address = True
    allow_reuse_port = True


class TCP6Server(TCPServer):
    address_family = AF_INET6


class WebsocketHandler(BaseRequestHandler):
    def setup(self):
        self.websocket = Websocket(self.server.get_websocket_url())
        self.websocket.connect()

        self.ws_to_socket_thread = threading.Thread(
            target = self.ws_to_socket, daemon = True
        )


    def handle(self):
        self.ws_to_socket_thread.start()

        self.socket_to_ws()
        self.websocket.close()

        self.ws_to_socket_thread.join()


    def finish(self):
        self.websocket.close()


    def socket_to_ws(self):
        while True:
            data = self.request.recv(4096)

            if not data:
                break

            try:
                self.websocket.write(data)
            except WebsocketError:
                break


    def ws_to_socket(self):
        while True:
            try:
                data = self.websocket.read()
            except WebsocketError:
                break

            if data is not None:
                self.request.sendall(data)


class Listener(threading.Thread):
    def __init__(self, bind, port, websocket_url_fn, *args, **kwargs):
        self.bind = bind
        self.port = port
        self.websocket_url_fn = websocket_url_fn
        self.server = None
        self.ready = threading.Event()

        super().__init__(*args, **kwargs)


    def run(self):
        Server = TCP6Server if ':' in self.bind else TCPServer

        with Server((self.bind, self.port), WebsocketHandler) as server:
            self.server = server
            self.server.get_websocket_url = self.websocket_url_fn

            self.ready.set()

            self.server.serve_forever() 


    def stop(self):
        if self.server is not None:
            self.server.shutdown()


class PortForwarder:
    def __init__(
        self, port, websocket_url_fn, client = None,
        quiet = True, bind = ('::1', '127.0.0.1'),
        command = None
    ):
        self.bind = bind
        self.port = port
        self.websocket_url_fn = websocket_url_fn
        self.client = client
        self.quiet = quiet
        self.command = command.replace(
            '%p', str(self.port)
        ).replace(
            '%h', self.bind[0]
        ) if command is not None else None

        self.exceptions = []

        threading.excepthook = self.exception_handler


    def exception_handler(self, args):
        if args.exc_type is OSError:
            exc = SystemError(
                args.exc_value.args[1], args.exc_value
            )
        else:
            exc = SystemError(
                args.exc_value, args.exc_value
            )

        self.exceptions.append(exc.with_traceback(args.exc_traceback))


    def check_exceptions(self):
        if self.exceptions:
            raise self.exceptions.pop(0)


    def run(self):
        self.threads = [
            Listener(bind, self.port, self.websocket_url_fn)
            for bind in self.bind
        ]

        for thread in self.threads:
            thread.start()

        while True:
            for thread in self.threads:
                if thread.ready.wait(0.1) is False:
                    break
            else:
                break

            self.check_exceptions()

        if not self.quiet and not self.command:
            print('Connect to localhost, port {}{}'.format(
                self.port,
                ', using a {}'.format(
                    self.client
                ) if self.client is not None else ''
            ))
            print('Press Ctrl+C to terminate')

        if self.command:
            with Popen(self.command, shell = True) as command:
                try:
                    command.communicate()   
                except KeyboardInterrupt:
                    print()

                    command.send_signal(signal.SIGINT)
                    command.communicate()

                if command.returncode < 0:
                    print('Command terminated by signal {}'.format(
                        -command.returncode
                    ))
                elif command.returncode != 0:
                    print('Command exited with status {}'.format(
                        command.returncode
                    ))
        else:
            try:
                while True:
                    sleep(0.5)

                    self.check_exceptions()
            except KeyboardInterrupt:
                if not self.quiet:
                    print('\nTerminating')

        try:
            for thread in self.threads:
                thread.stop()

            for thread in self.threads:
                thread.join()
        except KeyboardInterrupt:
            print('\nForcing termination')
            exit(0)

