#! /usr/bin/python3
#
# @(!--#) @(#) scrtrigger.py, sversion 0.1.0, version 003, 03-december-2020
#
# trigger a screenshot by sending a UDP packet to the pngshot.py program
#

import sys
import os
import socket

DEFAULT_UDP_PORT = 8333

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

sys.exit(0)

# end of file
