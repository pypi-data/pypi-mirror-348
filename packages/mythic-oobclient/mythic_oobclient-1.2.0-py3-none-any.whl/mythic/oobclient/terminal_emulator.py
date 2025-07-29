import urwid
import threading
import json
import atexit
import os
import time
import collections
import string

from .websocket import Websocket, WebsocketError
from .websocket_terminal import WebsocketTerminal
from .errors import TerminalError
from . import version, BAUD_RATES

DEFAULT_ESCAPE_CHARACTER = 'B'

class CommandError(Exception):
    pass


class CommandEdit(urwid.Edit):
    spinner_chars = '/-\|'
    spinner_update = 0.1


    def __init__(self, *args, **kwargs):
        self.main_loop = None
        self.spinner = None
        self.hide_spinner()

        super().__init__(*args, **kwargs)


    def get_text(self):
        text, attrib = super().get_text()

        return text + (self.spinner or ''), attrib


    def show_spinner(self):
        self.spinner_char = 0

        self.advance_spinner()


    def advance_spinner(self):
        if self.spinner_char is None:
            self.spinner = None

            return

        self.spinner = self.spinner_chars[self.spinner_char]
        self._invalidate()

        self.spinner_char += 1
        self.spinner_char %= len(self.spinner_chars)

        self.main_loop.set_alarm_in(
            self.spinner_update, lambda loop, data: self.advance_spinner()
        )


    def hide_spinner(self):
        self.spinner_char = None


    def enable_editing(self):
        self._can_edit = True


    def disable_editing(self):
        self._can_edit = False


    def reset(self):
        self.set_edit_text('')
        self.set_edit_pos(0)
        self.enable_editing()


    def keypress(self, size, key):
        if not self._can_edit:
            return

        if key == 'ctrl u':
            self.reset()
            return

        return super().keypress(size, key)


class TerminalEmulator:
    palette = dict(
        status = ('black', 'light gray'),
        command = ('white', 'dark blue'),
        error = ('white', 'light red'),
        line_high = ('white,bold', 'light blue'),
        line_low = ('black', 'light blue'),
        help = ('white', 'dark blue'),
        label = ('black', 'yellow'),
        size = ('black', 'white'),
        baud_rate = ('black', 'white')
    )

    max_state_websocket_retries = 30


    def help_text(self):
        sections = collections.defaultdict(list)

        sections['banner'].extend([
            '',
            'Client for Mythic Beasts OOB services',
            'Version {}'.format(version()),
        ])

        sections['head'].extend([
            'Commands:',
            '',
            '  reset         -- reset the terminal',
        ])

        if self.supports_baudrate:
            sections['serial'].extend([
                '  baud RATE     -- set baud rate to RATE',
                '                   (one of {})'.format(
                    ', '.join(str(rate) for rate in BAUD_RATES)
                )
            ])

        if self.supports_breaks:
            sections['serial'].extend([
                '  break         -- send break'
            ])

        if self.is_virtual:
            sections['power'].extend([
                '  shutdown      -- initiate ACPI shutdown',
                '  reboot        -- initiate ACPI reboot',
                '  power on      -- power server on',
                '  power off     -- forcefully power server off',
                '  power cycle   -- forcefully power-cycle server',
            ])
        elif self.is_physical:
            sections['power'].extend([
                '  power on      -- power server on',
                '  power off     -- power server off',
                '  power cycle   -- power-cycle server'
            ])

        sections['tail'].extend([
            '  quit          -- quit',
            '  help          -- show help',
        ])

        sections['escapes'].extend([
            'Escape sequences:',
            '',
            '  Ctrl+{0} Ctrl+{0} -- send a literal Ctrl+{0}'.format(
                self.escape_char
            ),
            '  Ctrl+{} PgUp   -- enter scroll mode'.format(self.escape_char),
            '',
            '  The default escape sequence is Ctrl+{}.'.format(
                DEFAULT_ESCAPE_CHARACTER
            ) if self.escape_char != DEFAULT_ESCAPE_CHARACTER else None,
            '  A custom escape character {} set using the -e command'.format(
                'can be' if self.escape_char == DEFAULT_ESCAPE_CHARACTER else 'has been'
            ),
            '  line flag, or the DEFAULT.EscapeCharacter configuration option.',
        ])

        sections['back'].extend([
            'Press any key to exit this help message',
        ])

        return '\n\n'.join(
            '\n'.join(
                '  {}'.format(line) for line in section if line is not None
            )
            for section in sections.values()
        )


    def __init__(self, identifier, api, escape_char = None):
        if escape_char is None:
            escape_char = DEFAULT_ESCAPE_CHARACTER
        self.identifier = identifier
        self.api = api

        if len(escape_char) != 1 or escape_char not in {*string.printable} - {*string.whitespace}:
            raise ValueError(
                'Escape character must be a single '
                'printable ASCII character'
            )
        self.escape_char = escape_char.upper()

        self.running = False
        self.running_task = None

        self.error = None
        self.error_pipe = None

        status = self.api.console_status(self.identifier)
        self.has_state = status.get('has_state', False)
        self.supports_baudrate = status.get('supports_baudrate', False)
        self.supports_breaks = status.get('supports_breaks', False)
        self.supports_line_state = status.get('supports_line_state', False)

        self.is_virtual = identifier.startswith('vds:')
        self.is_physical = not self.is_virtual

        self.state_websocket_retries = 0
        self.last_state_retry = 0

        self.history = self.api.console_log_tail(
            self.identifier, limit = 100,
            state_changes = False, timestamps = False
        )

        self.label = urwid.AttrMap(urwid.Text(
            ' {} '.format(self.api.normalise_identifier(self.identifier))
        ), 'label')
        self.baud_rate = urwid.AttrMap(
            urwid.Text('---bps '.rjust(11)),
            'baud_rate'
        )
        self.size = urwid.AttrMap(urwid.Text('?x?'), 'size')
        self.lines = {
            line: urwid.AttrMap(
                urwid.Text(' {} '.format(line.upper())),
                'line_low'
            )
            for line in ('dtr', 'rts', 'cts', 'dsr')
        }

        self.command = CommandEdit('> ')
        self.spinner = urwid.Text(' ')
        self.command_bar = urwid.AttrMap(urwid.Filler(self.command), 'command')

        serial_columns = []

        if self.supports_baudrate:
            serial_columns.append((11, self.baud_rate))

        if self.supports_line_state:
            serial_columns.extend(
                (len(line.original_widget.text), line)
                for line in self.lines.values()
            )

        self.status_bar = urwid.AttrMap(urwid.Filler(urwid.Columns([
            ('pack', self.label),
        ] + serial_columns + [
            ('pack', self.size)
        ], dividechars = 1)), 'status')

        self.help = urwid.AttrMap(urwid.Filler(
            urwid.Text(self.help_text()), valign = 'top'
        ), 'help')

        self.terminal = WebsocketTerminal(
            websocket_callback = lambda: Websocket(
                self.api.console_websocket(self.identifier)
            ),
            escape_sequence = 'ctrl {}'.format(self.escape_char.lower()),
            grab_callback = self.grab_callback,
            history = self.history
        )

        self.layout = urwid.Pile([
            ('weight', 1, self.terminal),
            (1, self.status_bar)
        ])

        self.loop = urwid.MainLoop(
            self.layout,
            [(name, *colours) for name, colours in self.palette.items()],
            input_filter = self.handle_pre_key,
            unhandled_input = self.handle_key,
            handle_mouse = False
        )

        self.error_pipe = self.loop.watch_pipe(self.handle_error)

        self.command.main_loop = self.loop

        self.terminal.main_loop = self.loop
        self.terminal.error_pipe = self.error_pipe
        self.terminal.keygrab = True

        self.set_size()

        self.state_pipe = None
        self.state_thread = None


    def handle_error(self, message):
        self.error = TerminalError(message.decode())

        raise urwid.ExitMainLoop()


    def connect_state_websocket(self, fail_silently = False):
        if not self.has_state:
            return

        try:
            state_websocket_url = self.api.state_websocket(self.identifier)

            if state_websocket_url is not None:
                self.state_websocket = Websocket(state_websocket_url)
                self.state_websocket.connect()
        except Exception:
            if fail_silently:
                self.state_websocket = None
            else:
                raise


    def run(self):
        urwid.set_encoding('utf8')

        self.running = True

        if self.has_state:
            self.state_pipe = self.loop.watch_pipe(self.set_state)

            self.connect_state_websocket()

            self.state_thread = threading.Thread(
                target = self.state_reader, daemon = True
            )
            self.state_thread.start()

        atexit.register(self.terminate)

        self.loop.run()

        if self.error is not None:
            raise self.error


    def terminate(self):
        self.running = False

        if self.has_state:
            self.state_websocket.close()


    def set_state(self, data):
        try:
            state = json.loads(data)
        except ValueError:
            return

        self.baud_rate.base_widget.set_text('{}bps '.format(
            state.get('baudrate', '---')
        ).rjust(11))

        for line, widget in self.lines.items():
            widget.attr_map = {
                None: 'line_{}'.format(
                    'high' if state.get(line) else 'low'
                )
            }


    def state_reader(self):
        while self.running:
            try:
                if self.state_websocket is None:
                    raise WebsocketError('no websocket')

                data = self.state_websocket.read()
            except WebsocketError:
                time.sleep(1)

                if time.time() - self.last_state_retry > 60:
                    self.state_websocket_retries = 0

                if self.state_websocket_retries < self.max_state_websocket_retries:
                    self.state_websocket_retries += 1

                    self.connect_state_websocket(fail_silently = True)

                    self.last_state_retry = time.time()
                else:
                    self.raise_error('Failed to reconnect to console')

                    return

                next

            if data is not None:
                os.write(self.state_pipe, data)


    def raise_error(self, message):
        if self.error_pipe is not None:
            os.write(self.error_pipe, message.encode())


    def set_size(self):
        cols, rows = self.loop.screen.get_cols_rows()

        self.size.base_widget.set_text(' {}x{} '.format(
            cols, rows - 1
        ))


    def run_background_task(self, task):
        self.command.disable_editing()
        self.command.show_spinner()

        self.running_task = threading.Thread(
            target = task
        )
        self.running_task.start()

        self.check_background_task()


    def check_background_task(self):
        if self.running_task is None:
            return

        if not self.running_task.is_alive():
            self.running_task.join()
            self.running_task = None

            self.command.hide_spinner()
            self.terminal.keygrab = True
        else:
            self.loop.set_alarm_in(
                0.1, lambda loop, data: self.check_background_task()
            )


    def process_command(self, command):
        if command == '':
            pass
        elif command == 'quit':
            raise urwid.ExitMainLoop()
        elif command in ('help', '?'):
            self.layout.contents[0] = (self.help, ('weight', 1))
        elif command == 'reset':
            self.terminal.term.reset()
            self.loop.draw_screen()
        elif self.supports_breaks and command == 'break':
            self.run_background_task(
                lambda: self.api.send_break(self.identifier)
            )
        elif self.supports_baudrate and command.startswith('baud '):
            _, baudrate = command.split(None, 1)

            if baudrate not in map(str, BAUD_RATES):
                raise CommandError('Invalid baud rate')

            self.run_background_task(
                lambda: self.api.set_baudrate(self.identifier, int(baudrate))
            )
        elif self.is_virtual and command == 'shutdown':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'off', force = False
                )
            )
        elif self.is_virtual and command == 'reboot':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'cycle', force = False
                )
            )
        elif self.is_virtual and command == 'power on':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'on'
                )
            )
        elif self.is_virtual and command == 'power off':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'off', force = True
                )
            )
        elif self.is_virtual and command == 'power cycle':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'cycle', force = True
                )
            )
        elif self.is_physical and command == 'power on':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'on'
                )
            )
        elif self.is_physical and command == 'power off':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'off'
                )
            )
        elif self.is_physical and command == 'power cycle':
            self.run_background_task(
                lambda: self.api.set_power(
                    self.identifier, 'cycle'
                )
            )
        else:
            raise CommandError('Unrecognised command')


    def handle_pre_key(self, keys, raw):
        if 'window resize' in keys:
            self.set_size()

        return keys


    def flash_command_error(self, restore = False):
        if restore:
            self.command_bar.attr_map = {None: 'command'}
        else:
            self.command_bar.attr_map = {None: 'error'}

            self.loop.set_alarm_in(
                0.2,
                lambda loop, data: self.flash_command_error(restore = True)
            )


    def grab_callback(self, terminal, grab):
        if not self.running:
            return

        if not grab:
            # Show the command bar when terminal is grab is released
            # (i.e., escape key is pressed), but keep the focus in
            # the terminal in case user wants to use a terminal escape
            # sequence.  If user types a key, we'll set the focus to
            # the command box when we handle the keypress.

            self.command.reset()
            self.change_layout(1, self.command_bar, focus = 0)
        else:
            # When terminal grab is enabled again, hide the command bar
            self.change_layout(1, self.status_bar, focus = 0)


    def handle_key(self, key):
        if self.layout_widget(0) is self.help:
            # Showing help widget instead of terminal;
            # any key escapes it and restores the terminal

            self.change_layout(0, self.terminal, focus = 0)

            return True

        if self.layout_widget(1) is self.command_bar:
            # Command bar is shown

            if key in ('enter', 'esc'):
                # Process enter/escape
                try:
                    if key == 'enter':
                        self.process_command(
                            self.command.get_edit_text().strip()
                        )
                except CommandError as err:
                    self.flash_command_error()
                else:
                    if self.running_task is None:
                        self.terminal.keygrab = True

                return True

        if len(key) == 1:
            # Otherwise, terminal grab is released and terminal
            # got a character it didn't process, so we assume
            # it's the first letter of a command, add it to the
            # command widget and focus it

            self.command.set_edit_text(key)
            self.command.set_edit_pos(1)

            self.layout.focus_position = 1

            return True


    def change_layout(self, position, widget, focus = None):
        old = self.layout.contents[position]

        new = list(old)
        new[0] = widget

        self.layout.contents[position] = tuple(new)

        if focus is not None:
            self.layout.focus_position = focus


    def layout_widget(self, position):
        return self.layout.contents[position][0]

