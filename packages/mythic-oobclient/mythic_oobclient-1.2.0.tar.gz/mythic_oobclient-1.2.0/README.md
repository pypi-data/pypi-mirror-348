# Mythic Beasts OOB client

This is a command-line utility that provides out-of-band access to virtual and
physical (dedicated or colo) servers running on Mythic Beasts infrastructure.

## Configuration

When you first run the client, it will create a template configuration file:

```
$ mythic-oob-client console vds:example
Please configure your API credentials in /home/user/.mythic/oob.conf
$ 
```

Edit this file and put in your API key and secret, which you can create in the
control panel, by
[clicking "API keys" on the home page](https://www.mythic-beasts.com/customer/api-users).

This key will need to have "Virtual Server Provisioning" and/or "Physical
Server Control" permissions.

It is also possible to use different API keys for virtual servers and physical
servers, if necessary.  See the template configuration file for more details.

## Usage

```
$ mythic-oob-client --help
usage: mythic-oob-client [-h] [-c CONFIG] [-q] [-d] {vnc,console,power} ...

Client for Mythic Beasts OOB services, version 1.0.0

positional arguments:
  {vnc,console,power}   Mode
    vnc                 Connect to VPS VNC console
    console             Connect to server serial console
    power               Server power control

options:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file path
  -q, --quiet           Quiet mode
  -d, --debug           Debug mode

Email support@mythic-beasts.com for help
```

## VPS virtual serial consoles and physical server serial consoles

This mode allows access to consoles in four different ways:

### Terminal emulator

This starts a terminal emulator connected to the console.  It features a status
bar at the bottom showing:

* The server name
* The baud rate (physical servers only)
* The status of serial lines (physical servers only)
* The window size

Pressing Ctrl+B will turn the status bar into a command prompt.  You can type
in 'help' and press enter to see a list of commands (for changing the baud
rate or sending a break) and escape sequences (for scrolling).

### Telnet port forwarding

This starts a listener on the specified port on localhost (both IPv6 and IPv4).
You can then connect to this port using a Telnet client to get access to the
console.

```
$ mythic-oob-client console -t 3000 vds:example
Connect to localhost, port 3000, using a Telnet client
Press Ctrl+C to terminate
```

Then, in another window:

```
$ telnet localhost 3000
Trying ::1...
Connected to localhost.
Escape character is '^]'.

example login: root
Password: 
Linux example.vs.mythic-beasts.com 6.1.0-17-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.69-1 (2023-12-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Jan  2 15:00:52 UTC 2025 on ttyS0
root@example:~# 
```

Terminate the Telnet session by pressing Ctrl+], typing q, and enter.  Then
press Ctrl+C in the first window to terminate the port forwarding.

Alternatively, you can spawn Telnet from inside the client and not have to
open a second window.  The client will exit once Telnet exits.

```
$ mythic-oob-client console -t 3000 -R 'telnet %h %p' vds:example
Trying ::1...
Connected to localhost.
Escape character is '^]'.

example login: root
Password: 
Linux example.vs.mythic-beasts.com 6.1.0-17-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.69-1 (2023-12-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Thu Jan  2 15:00:52 UTC 2025 on ttyS0
root@example:~# 
```

### Raw terminal

This puts your terminal in raw mode and connects it directly to the console.
There is no escape character to get out, so you will need to send a SIGTERM
from another window to end your session (which should reset your terminal back
to a working state), for example, using `pkill -f mythic-oob-client` (assuming
you only have one running).  If you need something that provides an escape
character, use terminal emulator mode instead.

```
$ mythic-oob-client console -r vds:example

example login: root
Password: 
Linux example.vs.mythic-beasts.com 6.1.0-17-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.69-1 (2023-12-30) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Fri Jan  3 15:12:04 UTC 2025 on ttyS0
root@example:~# 
```

### Raw port forwarding

This is similar to Telnet mode (above), but presents a raw connection, without
any Telnet control sequences.  This may be useful if you want to interact with
the console using your own script.

While it's possible to connect to the TCP port using a Telnet client, or
netcat, socat, etc., note that you will by default get local echo, meaning that
everything (that is echoed back by the remote end) you type will appear twice,
and passwords you enter will be visible.  If you just want to connect to the
console and type some commands, the other modes are much more useful.

### Viewing the console log

This mode prints the last lines of the console log, including timestamps for
each line and (for physical servers) lines to mark when the baud rate or serial
line state changed.

```
$ mythic-oob-client console -l 4 vds:example
2025-01-03 15:24:44: Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
2025-01-03 15:24:44: permitted by applicable law.
2025-01-03 15:24:44: Last login: Fri Jan  3 15:12:04 UTC 2025 on ttyS0
2025-01-03 15:24:44: root@example:~# 
$ 
```

### Usage

```
$ mythic-oob-client console --help
usage: mythic-oob-client console [-h] [-r | -t PORT | -p PORT | -l LINES]
                                 [-b {9600,19200,38400,57600,115200}] [-B]
                                 IDENTIFIER

positional arguments:
  IDENTIFIER            Service identifier or asset tag (e.g., vds:example,
                        dedicated:example, colo:example, B0000abcd)

options:
  -h, --help            show this help message and exit
  -r, --raw             Connect terminal to console in raw mode (send SIGTERM
                        to terminate)
  -t PORT, --telnet PORT
                        Forward console to local Telnet port
  -p PORT, --port PORT  Forward console to local TCP port
  -l LINES, --log LINES
                        Display last lines of console log
  -R COMMAND, --run COMMAND
                        Run specified command to connect to forwarded port;
                        port forwarding modes only (%h will be replaced by IP,
                        %p will be replaced by port number)
  -b {9600,19200,38400,57600,115200}, --baud {9600,19200,38400,57600,115200}
                        Set baud rate before connecting (physical server only)
  -B, --break           Send break before connecting (physical server only)

By default, starts a terminal emulator; once inside, press Ctrl+B, type
'help', and press enter for help
```

## VPS graphical (VNC) console

This mode starts a listener on localhost, by default on port 5900 (VNC display
0).  Connect to this port using a VNC viewer to view the graphical console of
the VPS.  Upon connection, the VNC password is displayed.

```
$ mythic-oob-client vnc vds:example
Connect to localhost, port 5900, using a VNC viewer
Press Ctrl+C to terminate
VNC password is: s9xqMVzp
```

You can also launch a VNC viewer from inside the client:

```
$ mythic-oob-client vnc -R 'ssvncviewer %h::%p' vds:example
VNC password is: s9xqMVzp
```

### Usage

```
$ mythic-oob-client vnc --help
usage: mythic-oob-client vnc [-h] [-p PORT] IDENTIFIER

positional arguments:
  IDENTIFIER            Service identifier of VPS (e.g., vds:example)

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Local listening port (default 5900)
  -R COMMAND, --run COMMAND
                        Run specified command to connect to forwarded port (%h
                        will be replaced by IP, %p will be replaced by port
                        number)
```

## Server power control

This mode allows controlling VPS power state, and physical server power,
thanks to remote-control PDUs in the datacentres.

### Listing power ports

This will print a list of power ports that the server has and their states.
These will almost always be labelled "0" and, for dual-powered servers, "1".
For a virtual server, there will always be a single port labelled "0".

For a single-powered server
```
$ mythic-oob-client power dedicated:example1 list
0: on
$
```

For a dual-powered server:
```
$ mythic-oob-client power dedicated:example2 list
0: on
1: on
$
```

For a virtual serer, it also shows the state in addition to on/off:
```
$ mythic-oob-client power vds:avfc1 list
0: on [running]
$
```

### Controlling power

The remaining commands allow you to turn power on or off, or power-cycle
physical servers, and to power on or off, shut down, or reboot virtual servers.

For a physical server, by default, the commands apply to all power ports, but a
specific port may be specified if necessary.

The command will ask for confirmation, but this can be skipped.

Power off a physical server:
```
$ mythic-oob-client power dedicated:example1 off
Power off server dedicated:example1? [yN] y
Server powered off
$ 
```

Power-cycle one port on a dual-powered server, skipping confirmation:
```
$ mythic-oob-client power dedicated:example2 cycle -p 1 -f
Server (port 1) power cycled
$ 
```

Shut down a virtual server:
```
$ mythic-oob-client power vds:example off
Shut down server vds:example? [yN] y
Server shutdown initiated
$ 
```

Forcefully power off a virtual server:

```
$ mythic-oob-client power vds:example off -F
Power off server vds:example? [yN] y
Server powered off
$ 
```

Reboot a virtual server:
```
$ mythic-oob-client power vds:avfc2 cycle
Reboot server vds:avfc2? [yN] y
Reboot initiated
$ 
```

Forcefully power-cycle a virtual server:
```
$ mythic-oob-client power vds:example cycle -F
Power-cycle server vds:example? [yN] y
Server powered off
Server powered on
$ 
```

### Usage

```
$ mythic-oob-client power --help
usage: mythic-oob-client power [-h] IDENTIFIER {list,on,off,cycle} ...

positional arguments:
  IDENTIFIER           Service identifier or asset tag (e.g.,
                       dedicated:example, colo:example, B0000abcd)
  {list,on,off,cycle}  Action
    list               List power ports and their states
    on                 Power server on
    off                Power server off
    cycle              Power-cycle server

options:
  -h, --help           show this help message and exit
```

```
$ mythic-oob-client power dedicated:example1 on --help
usage: mythic-oob-client power IDENTIFIER on [-h] [-p PORT] [-f]

options:
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Power port identifier (all ports if unspecified;
                        physical servers only)
  -f, --no-confirm      Skip confirmation
```

```
$ mythic-oob-client power dedicated:example1 off --help
usage: mythic-oob-client power IDENTIFIER off [-h] [-F] [-p PORT] [-f]

options:
  -h, --help            show this help message and exit
  -F, --force           Forcefully power off, as opposed to ACPI shutdown
                        (virtual servers only)
  -p PORT, --port PORT  Power port identifier (all ports if unspecified;
                        physical servers only)
  -f, --no-confirm      Skip confirmation
```

```
$ mythic-oob-client power dedicated:example1 cycle --help
usage: mythic-oob-client power IDENTIFIER cycle [-h] [-F] [-p PORT] [-f]

options:
  -h, --help            show this help message and exit
  -F, --force           Forcefully power-cycle, as opposed to ACPI reboot
                        (virtual servers only)
  -p PORT, --port PORT  Power port identifier (all ports if unspecified;
                        physical servers only)
  -f, --no-confirm      Skip confirmation
```

