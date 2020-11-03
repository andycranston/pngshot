# pngshot

A simple screenshot program to capture screenshots in PNG format.

## Overview

This Python 3 program uses the PyAutoGUI module to take screenshots.

It is for Windows only.

Screenshots are triggered by the receipt of a specially crafted UDP packet
so you will need a second system on your network to run the triggering
program.

## Known limitations

It does not work predictably (or even at all) on systems with more than one
display.

## Alternative screenshot program for Windows

If you need something with more features (like being able to trigger screenshots
by pressing keyboard sequences such as Alt plus Print Screen) then I recommend
Greenshot - visit:

[Greenshot](http://getgreenshot.org)

However, this is not the only alternative - visit:

[10 Best Screenshot Tools for Windows 10](https://www.bettertechtips.com/windows/screenshot-tool-windows-10/)

for more options.

## "So why pngshot?"

I have tried some of the screenshot programs available on
the Internet but I have yet to find one with this feature:

```
Trigger a screenshot when a request is sent over the network from another system
```

I am sure there are some screenshot programs available on the Internet that have
this feature. Let me know of any that do - I will be very grateful.

In the meantime I have implemented this feature in my `pngshot.py` screenshot
program.

Read on...

## Quick start

Open a command prompt and type:

```
python pngshot.py
```

A "spinner" appears - this is a repeating of sequence of the / - \ and | characters. You will
see the effect when you run the program. It means the `pngshot.py` program is ready to take
screenshots.

Copy the `scrtrigger.py` Python program to another system on your network that has
a Python 3 interpreter installed on it and type:

```
python scrtrigger.py 10.1.1.100
```

Change the IPv4 address `10.1.1.100` to the IP address of the system running the `pngshot.py`
program.

The `scrtrigger.py` program sends a specially crafted UDP packet over
the network on UDP port 8333 to the `pngshot.py` program. When the `pngshot.py`
program receieves this packet it takes a screenshot.

By default screenshots are saved in the current directory on the system running the `pngshot.py`
program.

The screenshots have a filename based on:

```
pngshot-YYYYMMDD-HHMMSS.png
```

where YYYY is the 4 digit year, MM is the 2 digit month number, DD is the 2 digit day of the
month, HH is the 2 digit hour in 24 hour clock notation, MM is the 2 digit minute and
SS is the 2 digit seconds. So the following screenshot file:

```
pngshot-20200930-171608.png
```

was taken on 30th September 2020 at sixteen minutes and 8 seconds past 5pm.

## Command line option -d / --dir

The command line option `-d` (or `--dir`) can be used to name a different directory
for the screenshot files to be saved in. For example:

```
python pngshot.py -d C:\TEMP
```

would put the screenshot files in the `C:\TEMP` directory on the system
running the `pngshot.py` program.

## Command line option -s / --seconds

Normally a screenshot is take as soon as the `pngshot.py` program receives
the specially crafted UDP packet.

However, the command line option `-s` (or `--seconds`) can be used to specify a number
of seconds to wait between the `pngshot.py` program
receiving the specially crafted UDP packet
and the screenshot being taken. For example:

```
python pngshot.py -s 5
```

would wait 5 seconds between receiving the UDP packet and taking the screenshot.

## Command line option -p / --port

By default the `pngshot.py` program listens for UDP packets on port 8333.
If you want the program to listen on a different port (perhaps
because another program is already using port 8333) then specify
a different port. For example:

```
python pngshot.py -p 6543
```

would listen on port 6543 instead.

This also means you need to specify the port number in addition to the IPv4 address
when using the `scrtrigger.py` program. For example:

```
python scrtrigger.py 10.1.1.100:6543
```

would send the specially crafted UDP packet to the `pngshot.py` program
running on the host with
IPv4 address `10.1.1.100` listening on UDP port 6543.

## Core code in the `scrtrigger.py` program

The Python 3 code to send the specially crafted UDP packet to the `pngshot.py`
program to trigger a screenshot can be reduced to:

```
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto('please take a screenshot now'.encode(), ('10.1.1.100', 8333))
sock.close()
```

This code segment sends the UDP packet to host with IPv4
address 10.1.1.100 using UDP port 8333.

Using this as a basis you can build your own program to trigger screenshots.

## The `pshot.py` and `pshot.css` files

There are two extra files in this repository which need a mention.

The `pshot.py` file is a Python 3 program that can be run on a web server as a CGI script
to allow screenshots to be triggered from a web page.

The `pshot.css` file is the CSS style sheet that `pshot.py` references.
It needs to be in the same directory as the `pshot.cgi` file.

And yes I know the CSS needs alot of work! As a friend of mine often says to
me: "for you Andy, CSS is just something that happens to other people". Very true :-)

Note that both of these file are under development but feel free to try them.

I have had success running `pshot.py` on the `lighttpd` ("lighty") web server as a CGI script using
a Python 3 interpreter. This was on virtual machine running OpenBSD version 6.6.

## Security notes

Depending on your systems (the one running the `pngshot.py` program and the one which
runs the `scrtrigger.py` program) you may need to configure firewalls to allow
the UDP traffic on port 8333 to flow between them. If you are using a different UDP port number
via the `-p` (or `--port`) command line option then take this into account.

When I say "specially crafted UDP packet" I simply mean one with the following
ASCII text in it:

```
please take a screenshot now
```

This means that any system that can send UDP packets to port 8333
(or whatever port number is being used by the `pngshot.py` program)
can trigger a screenshot.

If you think this poses a security risk to your environment then, quite simply,
do not use this software.


---------------------------------------------------
End of README.md
