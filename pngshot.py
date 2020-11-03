#
# @(!--#) @(#) pngshot.py, sversion 0.1.0, fversion 011, 03-november-2020
#
# a screenshot program by Andy Cranston for Windows
#
# saves screenshots in lossless PNG format.
# uses the PyAutoGUI Python libray.
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
import socket
import select

import pyautogui

############################################################################

DEFAULT_DEST_DIR = '.'
DEFAULT_UDP_PORT = 8333
SLEEP_INTERVAL  = 0.1
SPINNER_STRING  = '|/-\\'
PAYLOAD_STRING  = 'please take a screenshot now'

############################################################################

#
# Main
#

def main():
    global progname

    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dir',
                        help='directory to save screenshots to',
                        default=DEFAULT_DEST_DIR)
                        
    parser.add_argument('-s', '--seconds',
                        help='delay in seconds before taking screenshot',
                        type=int,
                        default=0)

    parser.add_argument('-p', '--port',
                        help='UDP port number to listen on',
                        type=int,
                        default=DEFAULT_UDP_PORT)
        
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print('{}: the path "{}" is not a directory'.format(progname, args.dir), file=sys.stderr)
        sys.exit(1)

    if not os.access(args.dir, os.W_OK):
        print('{}: the directory "{}" is not writable'.format(progname, args.dir), file=sys.stderr)
        sys.exit(1)
        
    udpport = args.port
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', udpport))
    packetpayload = PAYLOAD_STRING.encode()
        
    screenwidth, screenheight = pyautogui.size()
    if DEBUG:
        print('Screen resolution: {},{}'.format(screenwidth, screenheight))

    spinnerstring = SPINNER_STRING
    spinnercounter = 0
    
    while True:
        udppacketflag = False

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
       
        if udppacketflag:
            if args.seconds > 0:
                print('Waiting {} seconds before taking screen shot '.format(args.seconds), end='', flush=True)
                for i in range(0, args.seconds):
                    print('.', end='', flush=True)
                    time.sleep(1.0)
                print(' done')
                
            pngshotfilename = '{}\\pngshot-{:%Y%m%d-%H%M%S}.png'.format(args.dir, datetime.datetime.now())
            print('Taking screenshot {} ...'.format(pngshotfilename), end='', flush=True)
            pyautogui.screenshot(pngshotfilename)
            print(' done')
        else:
            print('{}\r'.format(spinnerstring[spinnercounter]), end='', flush=True)
            time.sleep(SLEEP_INTERVAL)
            spinnercounter += 1
            if spinnercounter >= len(spinnerstring):
                spinnercounter = 0

    # control never gets here!
    return 0

############################################################################

progname = os.path.basename(sys.argv[0])

try:
    sys.exit(main())
except KeyboardInterrupt:
    print('\rExiting')
    sys.exit(0)

# end of file
