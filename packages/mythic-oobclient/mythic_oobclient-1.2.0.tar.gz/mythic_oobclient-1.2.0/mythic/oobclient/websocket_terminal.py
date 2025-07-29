import urwid
import sys
import atexit
import threading
import os
import time

from urwid.vterm import KEY_TRANSLATIONS, KEY_TRANSLATIONS_DECCKM, ESC

from .websocket import WebsocketError


class WebsocketTerminal(urwid.Terminal):
    max_websocket_retries = 30

    def __init__(
        self,
        websocket_callback,
        *args,
        history = None,
        grab_callback = None,
        **kwargs
    ):
        self.websocket_callback = websocket_callback
        self.grab_callback = grab_callback
        self.history = history if type(history) == bytes else history.encode()

        # This prevents the main loop being set in the parent class __init__
        self.initialised = False
        self._main_loop = None

        super().__init__(None, *args, **kwargs)

        self.feed_thread = None
        self.websocket_retries = 0
        self.error_pipe = None
        self.last_retry = 0

        self.initialised = True


    def connect_websocket(self, fail_silently = False):
        try:
            self.websocket = self.websocket_callback()
            self.websocket.connect()
        except Exception:
            if fail_silently:
                self.websocket = None
            else:
                raise


    @property
    def main_loop(self):
        return self._main_loop


    @main_loop.setter
    def main_loop(self, value):
        if self.initialised:
            self._main_loop = value

        if self.main_loop is not None:
            self.feed_pipe = self.main_loop.watch_pipe(self.add_data)


    @property
    def keygrab(self):
        return self._keygrab


    @keygrab.setter
    def keygrab(self, value):
        value = bool(value)

        if not hasattr(self, '_keygrab') or self._keygrab != value:
            self._keygrab = value

            if self.grab_callback is not None:
                self.grab_callback(self, value)


    def spawn(self):
        self.connect_websocket()

        # This is a hack to make superclass methods (which check
        # self.pid is None and self.pid > 0) do the right thing
        self.pid = -1

        atexit.register(self.terminate)


    def add_watch(self):
        if self.history is not None:
            self.term.addstr(self.history)
            self.history = None

        self.feed()


    def remove_watch(self):
        pass


    def feed(self):
        if self.feed_thread is None:
            self.feed_thread = threading.Thread(
                target = self.feeder, daemon = True
            )

            self.feed_thread.start()


    def feeder(self):
        while not self.terminated:
            try:
                if self.websocket is None:
                    raise WebsocketError('no websocket')

                data = self.websocket.read()
            except WebsocketError:
                time.sleep(1)

                if time.time() - self.last_retry > 60:
                    self.websocket_retries = 0

                if self.websocket_retries < self.max_websocket_retries:
                    self.websocket_retries += 1

                    self.connect_websocket(fail_silently = True)

                    self.last_retry = time.time()
                else:
                    self.raise_error('Failed to reconnect to console')

                    return

                next

            if data is not None:
                os.write(self.feed_pipe, data)


    def raise_error(self, message):
        if self.error_pipe is not None:
            os.write(self.error_pipe, message.encode())


    def add_data(self, data):
        self.term.addstr(data)

        self.flush_responses()


    def terminate(self):
        super().terminate()

        self.websocket.close()


    def flush_responses(self):
        while self.response_buffer:
            data = self.response_buffer.pop(0).encode('utf8')

            try:
                self.websocket.write(data)
            except WebsocketError:
                break


    def set_termsize(self, width, height):
        pass


    # Annoyingly, this is a very long method in the superclass, of which
    # we only want to override the last line, so we have to copypaste :/
    def keypress(self, size, key):
        if self.terminated:
            return key

        if key == "window resize":
            width, height = size
            self.touch_term(width, height)
            return

        if (self.last_key == self.escape_sequence
            and key == self.escape_sequence):
            # escape sequence pressed twice...
            self.last_key = key
            self.keygrab = True
            # ... so pass it to the terminal
        elif self.keygrab:
            if self.escape_sequence == key:
                # stop grabbing the terminal
                self.keygrab = False
                self.last_key = key
                return
        else:
            if key == 'page up':
                self.term.scroll_buffer()
                self.last_key = key
                self._invalidate()
                return
            elif key == 'page down':
                self.term.scroll_buffer(up=False)
                self.last_key = key
                self._invalidate()
                return
            elif (self.last_key == self.escape_sequence
                  and key != self.escape_sequence):
                # hand down keypress directly after ungrab.
                self.last_key = key
                return key
            elif self.escape_sequence == key:
                # start grabbing the terminal
                self.keygrab = True
                self.last_key = key
                return
            elif self._command_map[key] is None or key == 'enter':
                # printable character or escape sequence means:
                # lock in terminal...
                self.keygrab = True
                # ... and do key processing
            else:
                # hand down keypress
                self.last_key = key
                return key
        self.last_key = key

        self.term.scroll_buffer(reset=True)

        if key.startswith("ctrl "):
            if key[-1].islower():
                key = chr(ord(key[-1]) - ord('a') + 1)
            else:
                key = chr(ord(key[-1]) - ord('A') + 1)
        else:
            if self.term_modes.keys_decckm and key in KEY_TRANSLATIONS_DECCKM:
                key = KEY_TRANSLATIONS_DECCKM.get(key)
            else:
                key = KEY_TRANSLATIONS.get(key, key)

        if key.startswith("meta "):
            subkey = key[5:]

            if self.term_modes.keys_decckm and key in KEY_TRANSLATIONS_DECCKM:
                subkey = KEY_TRANSLATIONS_DECCKM.get(subkey)
            else:
                subkey = KEY_TRANSLATIONS.get(subkey, subkey)

            key = ESC + subkey

        # ENTER transmits both a carriage return and linefeed in LF/NL mode.
        if self.term_modes.lfnl and key == "\x0d":
            key += "\x0a"

        key = key.encode(getattr(self, 'encoding', 'utf8'), 'ignore')

        try:
            self.websocket.write(key)
        except WebsocketError:
            pass

