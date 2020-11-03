# pngshot

A simple screenshot program to capture screenshots in lossless PNG format.

## Overview

This Python 3 program uses the PyAutoGUI module to take screenshots.

It is for Windows only.

Screenshots are triggered by the receipt of a specially crafted UDP packet so
you will need a second system on your network to run the triggering
program.

## Known limitations

It does not work predictably or even at all on systems with more than one display.

## Alternative screenshot program for Windows

If you need something with more features (like being able to trigger screenshots
by pressing keyboard sequences such as Alt plus Print Screen) then I recommend Greenshot - visit:

[Greenshot](http://getgreenshot.org)

However, this is not the only alternative - visit:

[10 Best Screenshot Tools for Windows 10](https://www.bettertechtips.com/windows/screenshot-tool-windows-10/)

for more options.

## "So why pngshot?"

Well I have tried some of the screenshot programs available on
the Internet and I am sure there are some that have this feature but I have yet to
find one with this feature:

```
Trigger a screenshot when a request is sent over the network from another system
```

I am sure there are some screenshot programs available on the Internet that have
this feature. Let me know of any that do - I will be very grateful.

In the meantime I have implemented this feature in my `pngshot.py` program.

Read on...

## Quick start

Open a command prompt and type:

```
python pngshot.py
```

A "spinner" appears - this is a repeating of sequence of the / - \ and | characters. You will
see the effect when you run the program. It basically means the program is ready to take
screenshots.

Copy the `scrtrigget.py` Python program to another system on your network that has
a Python 3 interpreter installed on it and type:

```
python scrtrigger.py 10.1.1.100
```

Change the IPv4 address `10.1.1.100` to the IP address of the system running the `pngshot.py`
program.

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

would put the screenshot files in the `C:\TEMP` directory.

## Command line option -s / --seconds

Normally a screenshot is take as soon as the `scrtrigger.py` program on the other
system has send the specially crafted UDP packet to the system running the `pngshot.py`
program.

However, the command line option `-s` (or `--seconds`) can be used to specify a number
of seconds to wait between the Num Lock key being pressed and the screenshot being taken.
For example:

```
python pngshot.py -s 5
```

would wait 5 seconds between pressing Num Lock and taking the screenshot. This can be handy
for situations where a certain sequence keyboard strokes need to be make to get the image required.

## Command line option -p / --port

By default the `pngshot.py` program
listens for UDP packets on port 8333. If you want to listen on a different port (perhaps
because another program is already using port 8333) then specify a different port. For example:

```
python pngshot.py -p 6543
```

would listen on port 6543 instead.

This also means you need to specify the port number as well as the IPv4 address when using
the `scrtrigger.py` program. In this case as follows:

```
python scrtrigger.py 10.1.1.100:6543
```



## Core code in the `scrtrigger.py` program

The Python 3 code to send a UDP packet to the `pngshot.py` program to trigger
a screenshot can be reduced to:

```
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto('please take a screenshot now'.encode(), ('10.1.1.100', 8333))
sock.close()
```

This code segment sends the UDP packet to host with IPv4 address 10.1.1.100 using UDP port 8333.

Using this as a basis you can build your own program to trigger screenshots.

## The `pshot.py` and `pshot.css` files

There are two extra files in this repository which need a mention.

The `pshot.py` file is a Python 3 program that can be run on a web server as a CGI script
to allow screenshots to be triggered from a web page.

The `pshot.css` file is the CSS style sheet that `pshot.py` references. At present I think
it takes away "style" rather than adding it :-)

Note that both of these file are under development but feel free to try them.

I have had success running `pshot.py` on the `lighttpd` ("lighty") web server as a CGI script using
a Python 3 interpreter. This was on virtual machine running OpenBSD version 6.6.

---------------------------------------------------
End of README.md
