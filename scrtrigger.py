#! /usr/bin/python3
#
# @(!--#) @(#) scrtrigger.py, version 002, 01-october-2020
#
# trigger a screenshot by sending a UDP packet to
# the scrshot.py program
#

########################################################################

import sys
import os
import socket

########################################################################

DEFAULT_UDP_PORT = 8333

########################################################################

#
# Main
#

def main():
    global progname

    if len(sys.argv) > 1:
        hostandudp = sys.argv[1]
    else:
        hostandudp = '127.0.0.1'

    fields = hostandudp.split(':')

    host = fields[0]

    if len(fields) >= 2:
        udp = int(fields[1])
    else:
        udp = DEFAULT_UDP_PORT

    print('Triggering screenshot on host {} using UDP port {}'.format(host, udp))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto('please take a screenshot now'.encode(), (host, udp))
    sock.close()

    print('Done')

    return 0

########################################################################

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
