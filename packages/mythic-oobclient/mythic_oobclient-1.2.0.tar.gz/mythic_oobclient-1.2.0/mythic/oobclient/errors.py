import os


class ClientError(Exception):
    exit_code = 1

    def __str__(self):
        return str(self.args[0])


class AuthError(ClientError):
    exit_code = os.EX_NOPERM


class IdentifierError(ClientError):
    exit_code = os.EX_DATAERR


class APIError(ClientError):
    exit_code = os.EX_UNAVAILABLE


class NotConfigured(ClientError):
    exit_code = os.EX_CONFIG


class SystemError(ClientError):
    exit_code = os.EX_SOFTWARE


class TerminalError(ClientError):
    exit_code = os.EX_SOFTWARE

