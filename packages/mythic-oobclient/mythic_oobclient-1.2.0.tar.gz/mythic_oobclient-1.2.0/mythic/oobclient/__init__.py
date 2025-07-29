BAUD_RATES = (9600, 19200, 38400, 57600, 115200)


def run():
    from .client import Client

    Client().run()


def version():
    from importlib import metadata

    try:
        return metadata.version('mythic_oobclient')
    except ImportError:
        return '?.?.?'

