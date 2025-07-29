from setuptools import setup, find_namespace_packages
from os import environ, path
from subprocess import check_output
from email import message_from_string


if path.exists('debian/changelog'):
    # Building a Debian package -- get the version from the changelog
    version = check_output(
        'dpkg-parsechangelog --show-field Version'.split()
    ).decode().strip().split('-')[0].split(':')[-1]
elif path.exists('PKG-INFO'):
    # Building from a Python source package -- get the version from PKG-INFO
    with open('PKG-INFO') as pkg_info:
        version = message_from_string(pkg_info.read()).get('Version')
else:
    # Building using our build script -- it will set the version based on git
    # tags
    # and fallback to dummy version for installing from git in a venv
    version = environ.get('VERSION', '0.0.0')

if version is None:
    raise ValueError('Failed to determine version')


setup(
    name = 'mythic-oobclient',
    version = version,
    license = 'GPL-3.0-or-later',
    author = 'Mythic Beasts',
    author_email = 'support@mythic-beasts.com',
    url = 'https://www.mythic-beasts.com/',
    description = 'Mythic Beasts OOB client',
    long_description = '''

Provides out-of-band access to servers running on Mythic Beasts
infrastructure, namely to:

 - VPS graphical (VNC) consoles
 - VPS virtual serial consoles
 - dedicated and colo server serial consoles
 - dedicated and colo server and VPS power control

    '''.strip(),
    packages = find_namespace_packages(include = ['mythic.*']),
    entry_points = {
        'console_scripts': [
            'mythic-oob-client = mythic.oobclient:run'
        ]
    },
    # Put these into stdeb.cfg too, otherwise they don't all get included as
    # dependencies of the deb package 
    install_requires = [
        'websocket-client >=0.53.0, <2.0.0',
        'urwid >=2.0.1, <3.0.0',
        'requests >=2.21.0, <3.0.0'
    ],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Console :: Curses',
        'Intended Audience :: System Administrators',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        'Topic :: System :: Systems Administration'
    ],
    keywords = ['Mythic Beasts', 'serial', 'VNC', 'OOB', 'power control']
)

