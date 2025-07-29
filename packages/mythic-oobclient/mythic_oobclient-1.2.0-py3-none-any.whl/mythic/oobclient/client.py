from os import EX_SOFTWARE
from argparse import ArgumentParser
from sys import stderr, exit

from .api_client import APIClient
from .config import Config
from .errors import ClientError
from .terminal_emulator import TerminalEmulator, DEFAULT_ESCAPE_CHARACTER
from .raw_terminal import RawTerminal
from .port_forwarder import PortForwarder
from . import version, BAUD_RATES


def confirm(prompt, default = False):
    while True:
        answer = input('{}? [{}] '.format(
            prompt,
            'Yn' if default is True else 'yN'
        )).strip().lower()

        if not answer:
            return default

        if answer in ('y', 'yes', 'yep'):
            return True
        elif answer in ('n', 'no', 'nope'):
            return False


class Client:
    def initialise_parser(
        self,
        enable_vnc = True,
        enable_console = True,
        enable_power = True
    ):
        self.parser_top = ArgumentParser(
            description = (
                'Client for Mythic Beasts OOB services, '
                'version {}'
            ).format(version()),
            epilog = 'Email support@mythic-beasts.com for help'
        )
        self.parser_top.add_argument(
            '-c', '--config', help = 'Config file path'
        )
        self.parser_top.add_argument(
            '-q', '--quiet', action = 'store_true',
            help = 'Quiet mode'
        )
        self.parser_top.add_argument(
            '-d', '--debug', action = 'store_true',
            help = 'Debug mode'
        )

        self.parser_command = self.parser_top.add_subparsers(
            help = 'Mode', dest = 'command', required = True
        )

        if enable_vnc:
            self.parser_vnc = self.parser_command.add_parser(
                'vnc',
                help = 'Connect to VPS VNC console'
            )
            self.parser_vnc.add_argument(
                '-p', '--port', type = int, default = 5900,
                help = 'Local listening port (default 5900)'
            )
            self.parser_vnc.add_argument(
                '-R', '--run', metavar = 'COMMAND',
                help = (
                    'Run specified command to connect to '
                    'forwarded port (%%h will be replaced by IP, '
                    '%%p will be replaced by port number)'
                )
            )
            self.parser_vnc.add_argument(
                'identifier', metavar = 'IDENTIFIER',
                help = 'Service identifier of VPS (e.g., vds:example)'
            )

        if enable_console:
            self.parser_console = self.parser_command.add_parser(
                'console',
                help = 'Connect to server serial console',
                epilog = (
                    "By default, starts a terminal emulator; once inside, "
                    "press Ctrl+{} (or selected escape character), "
                    "type 'help', and press enter for help".format(
                        DEFAULT_ESCAPE_CHARACTER
                    )
                )
            )
            self.parser_mode = self.parser_console.add_mutually_exclusive_group()
            self.parser_mode.add_argument(
                '-r', '--raw', action = 'store_true',
                help = (
                    'Connect terminal to console in raw mode '
                    '(send SIGTERM to terminate)'
                )
            )
            self.parser_mode.add_argument(
                '-t', '--telnet', type = int, metavar = 'PORT',
                help = 'Forward console to local Telnet port'
            )
            self.parser_mode.add_argument(
                '-p', '--port', type = int,
                help = 'Forward console to local TCP port'
            )
            self.parser_mode.add_argument(
                '-l', '--log', type = int, metavar = 'LINES',
                help = 'Display last lines of console log'
            )
            self.parser_console.add_argument(
                '-R', '--run', metavar = 'COMMAND',
                help = (
                    'Run specified command to connect to '
                    'forwarded port; port forwarding modes only '
                    '(%%h will be replaced by IP, '
                    '%%p will be replaced by port number)'
                )
            )
            self.parser_console.add_argument(
                '-b', '--baud', type = int,
                choices = BAUD_RATES,
                help = 'Set baud rate before connecting (physical server only)'
            )
            self.parser_console.add_argument(
                '-B', '--break', dest = 'send_break', action = 'store_true',
                help = 'Send break before connecting (physical server only)'
            )
            self.parser_console.add_argument(
                '-e', '--escape',
                help = 'Escape character in terminal emulator (default "{}", '
                        'can also be set using DEFAULT.EscapeCharacter '
                        'config option)'.format(DEFAULT_ESCAPE_CHARACTER)
            )
            self.parser_console.add_argument(
                'identifier', metavar = 'IDENTIFIER',
                help = (
                    'Service identifier or asset tag (e.g., vds:example, '
                    'dedicated:example, colo:example, B0000abcd)'
                )
            )

        if enable_power:
            self.parser_power = self.parser_command.add_parser(
                'power',
                help = 'Server power control'
            )
            self.parser_power.add_argument(
                'identifier', metavar = 'IDENTIFIER',
                help = (
                    'Service identifier or asset tag (e.g., vds:example, '
                    'dedicated:example, colo:example, B0000abcd)'
                )
            )
            self.parser_power_action = self.parser_power.add_subparsers(
                help = 'Action', dest = 'action'
            )
            self.parser_list_power = self.parser_power_action.add_parser(
                'list', help = 'List power ports and their states'
            )
            self.parser_power_on = self.parser_power_action.add_parser(
                'on', help = 'Power server on'
            )
            self.parser_power_off = self.parser_power_action.add_parser(
                'off', help = 'Power server off'
            )
            self.parser_power_off.add_argument(
                '-F', '--force', action = 'store_true',
                help = (
                    'Forcefully power off, as opposed to ACPI shutdown '
                    '(virtual servers only)'
                )
            )
            self.parser_power_cycle = self.parser_power_action.add_parser(
                'cycle', help = 'Power-cycle server'
            )
            self.parser_power_cycle.add_argument(
                '-F', '--force', action = 'store_true',
                help = (
                    'Forcefully power-cycle, as opposed to ACPI reboot '
                    '(virtual servers only)'
                )
            )
            for action in (
                self.parser_power_on, self.parser_power_off,
                self.parser_power_cycle
            ):
                action.add_argument(
                    '-p', '--port', default = None,
                    help = (
                        'Power port identifier (all ports if unspecified; '
                        'physical servers only)'
                    )
                )
                action.add_argument(
                    '-f', '--no-confirm', action = 'store_true',
                    help = 'Skip confirmation'
                )


    def parse_args(self):
        self.initialise_parser()

        self.args = self.parser_top.parse_args()


    def initialise(self):
        self.config = Config(filename = self.args.config)

        self.api = APIClient(
            auth_server = self.config.auth_server(),
            api_base = self.config.api_base(),
            credentials = self.config.credentials(),
            quiet = self.args.quiet
        )


    def run(self):
        try:
            self.parse_args()

            self.initialise()

            getattr(self, 'command_{}'.format(self.args.command))()
        except KeyboardInterrupt:
            print()
            exit(1)
        except ClientError as err:
            if self.args.debug:
                raise
            else:
                print(err, file = stderr)

                exit(err.exit_code)
        except Exception as err:
            if self.args.debug:
                print('Unhandled exception, this may be a bug:\n')

                raise
            else:
                print(err, file = stderr)

                exit(EX_SOFTWARE)


    def command_vnc(self):
        self.api.check_vps(self.args.identifier, warn = True)

        PortForwarder(
            port = self.args.port,
            websocket_url_fn = lambda: self.api.vnc_websocket(
                self.args.identifier
            ),
            quiet = self.args.quiet,
            client = 'VNC viewer',
            command = self.args.run
        ).run()


    def command_console(self):
        self.api.check_server(self.args.identifier)

        if self.args.baud is not None:
            self.api.set_baudrate(self.args.identifier, self.args.baud)

        if self.args.send_break:
            self.api.send_break(self.args.identifier)

        if self.args.telnet is not None:
            PortForwarder(
                port = self.args.telnet,
                websocket_url_fn = lambda: self.api.console_websocket(
                    self.args.identifier, 'telnet'
                ),
                quiet = self.args.quiet,
                client = 'Telnet client',
                command = self.args.run
            ).run()
        elif self.args.port is not None:
            PortForwarder(
                port = self.args.port,
                websocket_url_fn = lambda: self.api.console_websocket(
                    self.args.identifier
                ),
                quiet = self.args.quiet,
                command = self.args.run
            ).run()
        elif self.args.raw:
            RawTerminal(
                self.api.console_websocket(self.args.identifier)
            ).run()
        elif self.args.log:
            print(self.api.console_log_tail(
                self.args.identifier,
                limit = self.args.log,
                timestamps = True,
                state_changes = True
            ))
        else:
            TerminalEmulator(
                identifier = self.args.identifier,
                api = self.api,
                escape_char = self.args.escape or self.config.escape_char(),
            ).run()


    def command_power(self):
        prefix, name, data = self.api.check_server(self.args.identifier)

        force = getattr(self.args, 'force', False)

        if self.args.action == 'list':
            print(
                '\n'.join(
                    '{}: {}'.format(index, state)
                    for index, state in self.api.list_power_ports(
                        self.args.identifier
                    ).items()
                )
            )
        elif self.args.no_confirm or confirm(
            '{} server {}'.format(
                dict(
                    on = 'Power on',
                    off = (
                        'Shut down' if prefix == 'vds' and not force
                        else 'Power off'
                    ),
                    cycle = (
                        'Reboot' if prefix == 'vds' and not force
                        else 'Power-cycle'
                    )
                )[self.args.action],
                self.args.identifier
            )
        ):
            message = self.api.set_power(
                self.args.identifier, self.args.action,
                force, self.args.port
            )

            if not self.args.quiet:
                print(message)

