# pngshot

A simple screenshot program to capture screenshots in lossless PNG format.

## Overview

This Python 3 program uses the PyAutoGUI module to take screenshots.

It is for Windows only.

It has only a handful of features but it serves my purposes well.

## Known limitations

It does not work predictably or even at all on systems with more than one display.

## Alternative screenshot program for Windows

If you need something with more features I recommend Greenshot - visit:

[Greenshot](http://getgreenshot.org)

However, this is not the only alternative - visit:

[10 Best Screenshot Tools for Windows 10](https://www.bettertechtips.com/windows/screenshot-tool-windows-10/)

for more options.

## "So why pngshot?"

Well I have tried some (but not all) of the screenshot programs available on
the Internet and I am sure there are some that have this feature but I have yet to
find one with this feature:

```
Trigger a screenshot when a request is sent over the network from another system
```

Let me know of any screenshot programs that do this - I will be very grateful.

In the meantime I have implemented this feature in my `pngshot.py` program.

Read on...

## Quick start

Open a command prompt and type:

```
python pngshot.py
```

The program will say which directory the screenshots are going to be saved in - for example:

```
Screenshots will be saved in directory "C:\Users\Andy C\Pictures"
```

Next a "spinner" appears - this is a repeating of sequence of the / - \ and | characters. You will
see the effect when you run the program. It basically means the program is ready to take
screenshots.

To take a screenshot press the Num Lock key on the keyboard. The Num Lock light on your keyboard
will turn on. The program recognises
that the Num Lock key has been pressed and takes a screenshot and saves it to a
PNG file. It then automatically turns off Num Lock making the Num Lock light on your
keyboard turn off. This is how you know the program has taken a screenshot.

Screenshots are saved in the subdirectory called "Pictures" in the directory
named by the `USERPROFILE` environment variable. For example on my Windows 10
machine `USERPROFILE` is set to:

```
C:\Users\Andy C
```

so my screenshots are saved to the following subdirectory:

```
C:\Users\Andy C\Pictures
```

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

Normally a screenshot is take immediately after the Num Lock key is pressed.

However, the command line option `-s` (or `--seconds`) can be used to specify a number
of seconds to wait between the Num Lock key being pressed and the screenshot being taken.
For example:

```
python pngshot.py -s 5
```

would wait 5 seconds between pressing Num Lock and taking the screenshot. This can be handy
for situations where a certain sequence keyboard strokes need to be make to get the image required.

## Command line option -u / --udp

The command line option `-u` (or `--udp`) can be used to enable screenshots
to be triggered by sending special UDP packets to the `pngshot.py` program.
For example:

```
python pngshot.py -u
```

When running in this mode screenshots can still be triggered by pressing the Num Lock key
but they can also be triggered by running the `scrtrigger.py` program as follows:

```
python scrtrigger.py
```

This is only really useful if you copy the `scrtrigger.py` program to a different host
and run is as follows:

```
python scrtrigger.py 10.1.1.100
```

where 10.1.1.100 is the IPv4 address of the machine running the `pngshot.py` program.

This means from a second machine you can trigger a screenshot on the first machine. It just has
to be reachable on the network.

## Command line option -p / --port

By default the command line option `-u` (`--udp`) causes the `pngshot.py` program
to listen for UDP packets on port 8333. If you want to listen on a different port (perhaps
because another program is already using port 8333) then specify a different port. For example:

```
python pngshot.py -u -p 6543
```

would listen on port 6543 instead.

This also means you need to specify the port number as well as the IPv4 address when using
the `scrtrigger.py` program. In this case as follows:

```
python scrtrigger.py 10.1.1.100:6543
```

## "I always get NUM LOCK: ON in every screenshot"

Some Windows 10 systems display "NUM LOCK: ON" for a few seconds in the bottom right
hand corner of the screen whenever you press the Num Lock key. As a result this always
appears in every screenshot.

There are two ways around this.

First is to specify a delay of 6 or 7 seconds using the `-s` (`--seconds`) command line option.
The delay allows time for the message to disappear before actually taking the screenshot. It will,
however, slow you down in a way that will quickly become frustrating.

Second is to use the `scrtrigger.py` program on a second machine to trigger the
screenshots. However, you may not have a second machine handy for doing this.

Another approach is to tweak the Windows setup so it doesn't display "NUM LOCK: ON" in the
first place. It must be possible - if you know how please let me know so I can
update this README document - thankyou.

UPADTE:

This web page:

https://www.top-password.com/blog/disable-caps-lock-pop-up-notification-in-windows/

suggested some ways to turn off the "NUM LOCK: ON" messages. Unfortunately none
of them worked for my HP laptop but the suggestion that it might be to do
with Bluetooth got me looking at some other things. Looking at my installed
programs I noticed "CSR Harmony" software installed for a Bluetooth USB adapter
I no loner use. I uninstalled this software and now the "NUM LOCK: ON" messages
(and similar ones for CAPS Lock and Scroll Lock) are no longer displayed.
Problemn solved :-]



## Core code in the `scrtrigger.py` program

The actual Python 3 code to send a UDP packet to the `pngshot.py` program to trigger
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
