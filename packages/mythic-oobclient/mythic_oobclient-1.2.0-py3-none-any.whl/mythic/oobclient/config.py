from configparser import ConfigParser, Error as ConfigError
from pathlib import Path
from os import environ

from .errors import NotConfigured


AUTH_SERVER_URL = 'https://auth.mythic-beasts.com/'
API_BASE_URL = 'https://api.mythic-beasts.com/'

SAMPLE_CONFIG = '''
; Get an API key from https://www.mythic-beasts.com/customer/api-users
; and put it here
[DEFAULT]
;KeyID = 34xakvkwqxxzfgy8
;Secret = QR7AB6E9xJyK5zg3RgGcuUutS_9sEt

; Uncomment either or both of these sections to use different
; API keys for VPSs and physical servers
;[VPS]
;KeyID = 34xakvkwqxxzfgy8
;Secret = QR7AB6E9xJyK5zg3RgGcuUutS_9sEt
;
;[Physical]
;KeyID = 34xakvkwqxxzfgy8
;Secret = QR7AB6E9xJyK5zg3RgGcuUutS_9sEt
'''.lstrip()

class Config:
    def __init__(self, filename = None):
        if filename is not None:
            self.filename = Path(filename)
        else:
            self.filename = Path(
                environ['HOME'], '.mythic', 'oob.conf'
            )

        try:
            if not self.filename.exists():
                self.filename.parent.mkdir(parents = True, exist_ok = True)
                self.filename.write_text(SAMPLE_CONFIG)
        except OSError as err:
            raise NotConfigured(
                'Error reading configuration: {}'.format(err.args[1]),
                err
            )

        self.settings = ConfigParser()
        try:
            with self.filename.open('r') as config_file:
                self.settings.read_file(config_file)
        except OSError as err:
            raise NotConfigured(
                'Error reading configuration: {}'.format(err.args[1]),
                err
            )
        except ConfigError as err:
            raise NotConfigured(
                'Configuration error:\n{}'.format(err),
                err
            )

        for section in ('VPS', 'Physical'):
            if not self.settings.has_section(section):
                self.settings.add_section(section)

        if (
            not self.settings.has_option('VPS', 'KeyID')
            or not self.settings.has_option('VPS', 'Secret')
        ) and (
            not self.settings.has_option('Physical', 'KeyID')
            or not self.settings.has_option('Physical', 'Secret')
        ):
            raise NotConfigured(
                'Please configure your API credentials in {}'.format(
                    self.filename
                )
            )


    def credentials(self):
        return dict(
            vps = (
                self.settings.get('VPS', 'KeyID', fallback = None),
                self.settings.get('VPS', 'Secret', fallback = None)
            ),
            physical = (
                self.settings.get('Physical', 'KeyID', fallback = None),
                self.settings.get('Physical', 'Secret', fallback = None)
            )
        )


    def auth_server(self):
        return self.settings.get(
            'DEFAULT', 'AuthServer', fallback = AUTH_SERVER_URL
        )


    def api_base(self):
        return self.settings.get(
            'DEFAULT', 'APIBase', fallback = API_BASE_URL
        )

    def escape_char(self):
        return self.settings.get(
            'DEFAULT', 'EscapeCharacter', fallback = None
        )
