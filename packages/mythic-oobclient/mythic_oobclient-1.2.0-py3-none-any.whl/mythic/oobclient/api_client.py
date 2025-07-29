from functools import wraps
from requests import Session, RequestException
from datetime import datetime, timedelta
from time import sleep

from .errors import AuthError, IdentifierError, APIError, NotConfigured
from . import version


HEADERS = {
    'User-Agent': 'mythic-oob-client/{}'.format(version())
}


def is_mythic_id(name):
    return len(name) == 9 and name.startswith('B')


def identifier(kind, return_none = False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(self, identifier, *args, **kwargs):
            if ':' in identifier:
                prefix, name = identifier.split(':', 1)
            elif kind == 'vps':
                prefix = 'vds'
                name = identifier
            elif is_mythic_id(identifier):
                prefix = 'dedicated'
                name = identifier
            else:
                raise IdentifierError('Invalid service identifier')

            if prefix not in ('dedicated', 'colo', 'vds'):
                raise IdentifierError(
                    "Invalid service identifier prefix '{}'".format(prefix)
                )

            if prefix in (
                'dedicated', 'colo'
            ) and kind not in (
                'any', 'physical'
            ):
                if return_none:
                    return None

                raise IdentifierError(
                    'Invalid service identifier; must be a VPS'
                )

            if prefix == 'vds' and kind not in ('any', 'vps'):
                if return_none:
                    return None

                raise IdentifierError(
                    'Invalid service identifier; must be a physical server'
                )

            return fn(self, prefix, name, *args, **kwargs)

        return wrapper

    return decorator


class APIClient:
    def __init__(self, auth_server, api_base, credentials, quiet = True):
        self.auth_server = auth_server.rstrip('/')
        self.api_base = api_base.rstrip('/')
        self.quiet = quiet
        self.credentials = credentials
        self.session = Session()

        self.auth_token = {}
        self.auth_token_expiry = {}
        self.last_vnc_password = None


    def authenticate(self, kind):
        if self.auth_token.get(kind) is not None and (
            self.auth_token_expiry.get(kind) - datetime.now()
        ) > timedelta(seconds = 30):
            return

        if any(credential is None for credential in self.credentials[kind]):
            raise NotConfigured(
                'No credentials configured for {}'.format(
                    dict(
                        physical = 'physical servers',
                        vps = 'VPSs'
                    )[kind]
                )
            )

        try:
            response = self.session.request('post', '{}/login'.format(
                self.auth_server
            ), auth = self.credentials[kind], data = dict(
                grant_type = 'client_credentials'
            ), headers = HEADERS)
        except RequestException as err:
            raise AuthError(
                'Error connecting to authentication service', err
            )

        if not response.ok:
            raise AuthError(
                'Failed to authenticate; check your API credentials', response
            )

        try:
            auth_data = response.json()
        except ValueError:
            raise AuthError('Invalid response from API', response)

        self.auth_token[kind] = auth_data['access_token']
        self.auth_token_expiry[kind] = datetime.now() + timedelta(
            seconds = auth_data['expires_in']
        )


    def api_request(self, kind, method, path, body = None):
        self.authenticate(kind)

        try:
            response = self.session.request(
                method,
                '{}/{}'.format(self.api_base, path),
                headers = dict(Authorization = 'Bearer {}'.format(
                    self.auth_token[kind]
                ), **HEADERS),
                json = body
            )
        except RequestException as err:
            raise AuthError(
                'Error connecting to API', err
            )

        try:
            data = response.json()
        except ValueError:
            raise APIError('Invalid response from API', response)

        if not response.ok:

            if 'error' in data and data['error']:
                message = data['error']
            else:
                message = 'Unspecified API error ({} {})'.format(
                    response.status_code, response.reason
                )

            raise APIError(message, response)

        return data


    @identifier('any')
    def set_power(self, prefix, name, state, force = False, port = None):
        if prefix == 'vds':
            if state in ('on', 'off'):
                if state == 'on':
                    power = 'power-on'
                elif force:
                    power = 'power-off'
                else:
                    power = 'shutdown'

                data = self.api_request(
                    'vps', 'put',
                    'beta/vps/servers/{}/power'.format(
                        name
                    ),
                    dict(power = power)
                )

                return data['message']
            elif force:
                data_off = self.api_request(
                    'vps', 'put',
                    'beta/vps/servers/{}/power'.format(
                        name
                    ),
                    dict(power = 'power-off')
                )

                sleep(1)

                data_on = self.api_request(
                    'vps', 'put',
                    'beta/vps/servers/{}/power'.format(
                        name
                    ),
                    dict(power = 'power-on')
                )

                return '\n'.join(
                    data['message'] for data in (data_off, data_on)
                )
            else:
                data = self.api_request(
                    'vps', 'post',
                    'beta/vps/servers/{}/reboot'.format(
                        name
                    )
                )

                return data['message']
        else:
            data = self.api_request(
                'physical', 'put', 'beta/{}/servers/{}/power{}'.format(
                    prefix, name,
                    '/{}'.format(port) if port is not None else ''
                ),
                dict(power = state)
            )

            return data['message']


    @identifier('any')
    def list_power_ports(self, prefix, name):
        if prefix == 'vds':
            data = self.api_request(
                'vps', 'get', 'beta/vps/servers/{}'.format(name)
            )

            return {'0': '{} [{}]'.format(
                'on' if data['status'] in (
                    'running', 'shutting down'
                ) else 'off',
                data['status']
            )}
        else:
            data = self.api_request(
                'physical', 'get', 'beta/{}/servers/{}/power'.format(prefix, name)
            )

            return {
                port['index']: port['state']
                for port in data['power_ports']
            }


    @identifier('any')
    def console_status(self, prefix, name):
        if prefix == 'vds':
            data = self.api_request(
                'vps', 'get',
                'beta/vps/servers/{}/console'.format(
                    name
                )
            )
        else:
            data = self.api_request(
                'physical', 'get',
                'beta/{}/servers/{}/console'.format(
                    prefix, name
                )
            )

        return data


    @identifier('any')
    def console_websocket(self, prefix, name, kind = 'serial'):
        if prefix == 'vds':
            data = self.api_request(
                'vps', 'get',
                'beta/vps/servers/{}/console/websocket?type={}'.format(
                    name, kind
                )
            )
        else:
            data = self.api_request(
                'physical', 'get',
                'beta/{}/servers/{}/console/websocket?type={}'.format(
                    prefix, name, kind
                )
            )

        return data['url']


    @identifier('physical', return_none = True)
    def state_websocket(self, prefix, name):
        data = self.api_request(
            'physical', 'get',
            'beta/{}/servers/{}/console/websocket?type=state'.format(prefix, name)
        )

        return data['url']


    @identifier('any')
    def console_log_tail(
            self, prefix, name, limit = 100,
            timestamps = False, state_changes = False
        ):
        query = 'limit={}&timestamps={}&state_changes={}'.format(
            limit,
            1 if timestamps else 0,
            1 if state_changes else 0
        )

        if prefix == 'vds':
            data = self.api_request(
                'vps', 'get',
                'beta/vps/servers/{}/console/log?{}'.format(name, query)
            )
        else:
            data = self.api_request(
                'physical', 'get',
                'beta/{}/servers/{}/console/log?{}'.format(prefix, name, query)
            )

        return data['console_output']


    @identifier('vps')
    def vnc_websocket(self, prefix, name):
        data = self.api_request(
            'vps', 'get',
            'beta/vps/servers/{}/vnc'.format(name)
        )

        password = data.get('password')

        if password != self.last_vnc_password:
            self.last_vnc_password = password

            if not self.quiet:
                if password:
                    print('VNC password is: {}'.format(password))
                else:
                    print('VNC password is blank')

        return data['url']


    @identifier('physical')
    def set_baudrate(self, prefix, name, baudrate):
        self.api_request(
            'physical', 'put',
            'beta/{}/servers/{}/console'.format(prefix, name),
            dict(
                baudrate = baudrate
            )
        )


    @identifier('physical')
    def send_break(self, prefix, name):
        self.api_request(
            'physical', 'put',
            'beta/{}/servers/{}/console/break'.format(prefix, name)
        )


    @identifier('vps')
    def check_vps(self, prefix, name, warn = False):
        data = self.api_request(
            'vps', 'get', 'beta/vps/servers/{}'.format(name)
        )

        if warn and not self.quiet and data.get('status') != 'running':
            print('Warning: VPS is not running')

        return prefix, name, data


    @identifier('any')
    def check_server(self, prefix, name, warn = False):
        if prefix == 'vds':
            return prefix, name, self.check_vps(name, warn)
        else:
            return prefix, name, self.api_request(
                'physical', 'get', 'beta/{}/servers/{}'.format(prefix, name)
            )


    @identifier('any')
    def normalise_identifier(self, prefix, name):
        if prefix == 'dedicated' and is_mythic_id(name):
            return name
        else:
            return '{}:{}'.format(prefix, name)

