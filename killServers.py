import time
import random
import socket
import threading

import traceback
import sys

from plugins_stuff import ConnectHandle

c_1 = ConnectHandle( client=True, port=14517 )
c_2 = ConnectHandle( client=True, port=14518 )


KILL_SERVER = bytes( [0xff] )
#LIST = [2, 103, 0, 0, 0, 168, 137, 211, 213, 87, 92, 227, 147, 241, 115, 130, 138, 105, 174, 116, 241, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 240]

#c_1.clientSend( bytes([0x02, 0x68, 0x00, 0x00, 0x00] + LIST + [ 0xf0 ]) )
#c_1.clientSend( bytes([0x02, 0x67, 0x00, 0x00, 0x00] + LIST + [ 0xf0 ]) )

#c_2.clientSend( bytes([0x02, 0x68, 0x00, 0x00, 0x00] + LIST + [ 0xf0 ]) )
#c_2.clientSend( bytes([0x02, 0x67, 0x00, 0x00, 0x00] + LIST + [ 0xf0 ]) )

#time.sleep(10)

c_1.clientSend( KILL_SERVER )
c_2.clientSend( KILL_SERVER )

"""
c_threads = []

c_threads.append(
    threading.Thread(
            target=c_1.clientSend,
            args=( bytes([0x01, 0x67, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA1, 0xA1, 0xA1, 0xF0]),)
            )
    )
c_threads.append(
    threading.Thread(
            target=c_2.clientSend,
            args=( bytes([0x02, 0x67, 0x00, 0x00, 0x00, 0x00, 0x00, 0xA1, 0xA1, 0xA1, 0xF0]),)
            )
    )


print('Starting threads:')

print("\tclient")
for cTh in c_threads:
    cTh.start()
    #time.sleep(1)

print('Waiting threads to finish')

print("\tclients")
for cTh in c_threads:
    cTh.join()
"""

