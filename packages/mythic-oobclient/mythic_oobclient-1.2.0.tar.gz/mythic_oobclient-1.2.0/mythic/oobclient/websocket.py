from websocket import create_connection, ABNF, WebSocketException
from ssl import SSLError


class WebsocketError(Exception):
    pass


class Websocket:
    def __init__(self, websocket_url):
        self.websocket_url = websocket_url
        self.websocket = None


    def connect(self):
        self.websocket = create_connection(self.websocket_url)


    def read(self):
        try:
            opcode, data = self.websocket.recv_data()
        except (WebSocketException, SSLError) as err:
            raise WebsocketError(err)

        if opcode in (
            ABNF.OPCODE_TEXT, ABNF.OPCODE_BINARY
        ):
            return data
        else:
            return None


    def write(self, data):
        if self.websocket is None:
            return

        try:
            self.websocket.send(data, opcode = ABNF.OPCODE_BINARY)
        except (WebSocketException, SSLError) as err:
            raise WebsocketError(err) 


    def close(self):
        if self.websocket is not None:
            self.websocket.close()

