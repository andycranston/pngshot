#!/usr/local/bin/python3

#
# @(#) @(!--#) shot.py, version 002, 27-september-2020
#
# trigger a screenshot on a remote Windows desktop which
# is running the pngshot.py program with the --udp option
#

##############################################################################

DEBUG = True

##############################################################################

#
# imports
#

import sys
import os
import time
import datetime
import cgi
import cgitb; cgitb.enable()  # for troubleshooting
import html
import socket

##############################################################################

#
# constants
#

DEFAULT_IP_ADDRESS = '10.1.1.100'
DEFAULT_UDP_PORT = '8333'

##############################################################################

#
# Main
#

def main():
    global progname

    form = cgi.FieldStorage()

    ipaddress   = form.getfirst('ipaddress', DEFAULT_IP_ADDRESS)
    portnumber  = form.getfirst('portnumber', DEFAULT_UDP_PORT)
    trigger     = form.getfirst('trigger', '')

    pagetitle = 'Screenshot remote control'

    cssname = progname.split('.')[0] + '.css'

    print('Content-type: text/html')
    print('')

    print('<head>')
    print('<meta charset="utf-8">')
    print('<link rel="stylesheet" type="text/css" href="{}">'.format(cssname))
    print('<title>{}</title>'.format(pagetitle))
    print('</head>')

    print('<body>')

    print('<h1>{}</h1>'.format(pagetitle))

    if trigger != '':
        print('<p class="triggered">')

        print('Triggered screenshot')
        print('<br>')
        print('at {:%H%:%M:%S}'.format(datetime.datetime.now()))

        payloadstring = 'please take a screenshot now'
        payloadpacket = bytearray(len(payloadstring))
        for i in range(0, len(payloadstring)):
            payloadpacket[i] = ord(payloadstring[i])

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(payloadpacket, (ipaddress, int(portnumber)))
        sock.close()

        print('</p>')

    print('<form method="post" action="{}">'.format(progname))

    print('</p>')

    print('IP Address: <input type="text" name="ipaddress" size="16" value="{}">'.format(html.escape(ipaddress)))

    print('<br>')
    print('<br>')

    print('Port: <input type="text" name="portnumber" size="6" value="{}">'.format(html.escape(portnumber)))

    print('<br>')
    print('<br>')

    print('<input type="submit" name="trigger" value="Trigger">')

    print('</p>')

    print('</form>')

    print('</body>')

    return 0

##############################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
