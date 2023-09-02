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

# Server threads stoppers
c_1.clientSend( KILL_SERVER )
c_2.clientSend( KILL_SERVER )

"""
c_threads = []

c_threads.append(
    threading.Thread(
            target=c_1.clientSend,
            args=( bytes([0x01, 0x67, 0x00, 0x00, 0x00, 0x00, 0x00, 0x15, 0x15, 0x15, 0xF0]),)
            )
    )
c_threads.append(
    threading.Thread(
            target=c_2.clientSend,
            args=( bytes([0x02, 0x67, 0x00, 0x00, 0x00, 0x00, 0x00, 0x15, 0x15, 0x15, 0xF0]),)
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

