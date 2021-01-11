#
# @(!--#) @(#) pngshot.py, sversion 0.1.0, fversion 013, 10-january-2021
#
# a screenshot program by Andy Cranston for Windows
#
# saves screenshots in lossless PNG format. uses the PyAutoGUI Python libray
#
# Links:
# -----
#
#    https://www.simplifiedpython.net/python-screenshot/
#    https://stackoverflow.com/questions/34028478/python-3-detect-caps-lock-status
#    https://docs.microsoft.com/en-us/windows/win32/inputdev/virtual-key-codes
#

############################################################################

DEBUG = False

############################################################################

import sys
import os
import argparse
import time
import datetime
import ctypes
import socket
import select
import pyautogui

############################################################################

DEFAULT_UDP_PORT = 8333
VK_NUMLOCK = 0x90
SLEEP_INTERVAL = 0.1
WATCHDOG_STRING = '/-\\|'
PAYLOAD_STRING = 'please take a screenshot now'

############################################################################

def string2bytearray(s):
    ba = bytearray(len(s))

    for i in range(0, len(s)):
        ba[i] = ord(s[i])

    return ba

############################################################################

#
# Main
#

def main():
    global progname

    try:
         userprofile = os.environ['USERPROFILE']
    except KeyError:
         userprofile = 'C:'

    defaultdir = userprofile + '\\Pictures'

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dir',
                        help='directory to save screenshots to',
                        default=defaultdir)
                        
    parser.add_argument('-s', '--seconds',
                        help='delay in seconds before taking screenshot',
                        type=int,
                        default=0)

    parser.add_argument('-p', '--port',
                        help='UDP port number to listen on',
                        type=int,
                        default=DEFAULT_UDP_PORT)
        
    parser.add_argument('-u', '--udp',
                        help='listen for UDP screen shot request packets',
                        action='store_true')
    
    args = parser.parse_args()

    destdir = args.dir

    if not os.path.isdir(destdir):
        print('{}: the path "{}" is not a directory'.format(progname, destdir), file=sys.stderr)
        sys.exit(1)

    if not os.access(destdir, os.W_OK):
        print('{}: the directory "{}" is not writable'.format(progname, destdir), file=sys.stderr)
        sys.exit(1)
    
    print('Screenshots will be saved in directory "{}"'.format(destdir))
        
    delay = args.seconds
    
    udpport = args.port
    
    if args.udp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', udpport))
        packetpayload = string2bytearray(PAYLOAD_STRING)
        
    user32 = ctypes.WinDLL('user32')
    user32.GetKeyState.restype = ctypes.c_short
                
    screenwidth, screenheight = pyautogui.size()
    
    if DEBUG:
        print('Screen resolution: {},{}'.format(screenwidth, screenheight))

    watchdogstring = WATCHDOG_STRING
    watchdogcounter = 0
    
    lastkeystate = user32.GetKeyState(VK_NUMLOCK) & 0x0001
    if DEBUG:
        print(lastkeystate)
    
    if lastkeystate == 1:
        if DEBUG:
            print('Switching NUM LOCK off')
        pyautogui.press('numlock')
        time.sleep(SLEEP_INTERVAL)
        if DEBUG:
            print('Done')

    while True:
        keystate = user32.GetKeyState(VK_NUMLOCK) & 0x0001
        if DEBUG:
            print(keystate)
        
        numlockflag = False
        if (keystate == 1) and (lastkeystate == 0):
            numlockflag = True
        
        udppacketflag = False
        if args.udp:
            rlist, wlist, xlist = select.select([sock], [], [], 0.0)
            if DEBUG:
                print(rlist)
            if len(rlist) > 0:
                try:
                    packet, address = sock.recvfrom(65536)
                    if len(packet) == len(packetpayload):
                        if packet == packetpayload:
                            udppacketflag = True
                except ConnectionResetError:
                    print("{}: connecton reset error - going again".format(progname), file=sys.stderr)
       
        if numlockflag or udppacketflag:
            if delay > 0:
                print('Waiting {} seconds before taking screen shot '.format(delay), end='', flush=True)
                for i in range(0, delay):
                    print('.', end='', flush=True)
                    time.sleep(1.0)
                print(' done')
                
            pngshotfilename = '{}\\pngshot-{:%Y%m%d-%H%M%S}.png'.format(destdir, datetime.datetime.now())
            print('Taking screenshot {} ...'.format(pngshotfilename), end='', flush=True)
            pyautogui.screenshot(pngshotfilename)
            if numlockflag:
                pyautogui.press('numlock')
            print(' done')
        else:
            print('{}\r'.format(watchdogstring[watchdogcounter]), end='', flush=True)
            time.sleep(SLEEP_INTERVAL)
            watchdogcounter += 1
            if watchdogcounter >= len(watchdogstring):
                watchdogcounter = 0
                        
        lastkeystate = keystate

    return 0

############################################################################

progname = os.path.basename(sys.argv[0])

try:
    sys.exit(main())
except KeyboardInterrupt:
    print('\rExiting')
    sys.exit(0)

# end of file
