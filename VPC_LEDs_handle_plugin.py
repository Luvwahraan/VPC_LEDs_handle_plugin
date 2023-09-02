import hid
import time
import random
import socket
import threading

import traceback
import sys

from plugins_stuff import ConnectHandle
from Virpil import *

"""
    I use Virpil HOSAS, with control panels:
        left Constellation Alpha Prime, with Control Panel #2 in slave.
        right Constellation Alpha Prime, with Control Panel #1 in slave.
"""




def getRandomColor():
    return random.randrange(64, 256)


class Multi_Device_Handler():
    """
    Handle multiple Virpil_device object.
    
    
    Attributes
    ----------
    _device
        dictionnary: { deviceName: {device: Virpil_device, connexion: bool }
        Setting update to True will cause update at next iteration
    
    Methods
    -------
    
    
    """

    def __init__(self):
        self._devices = {}
        self._threads = {}
        threading.Thread.__init__(self)
    
    
    def addDevice(self, name, device):
        if not isinstance( device, Virpil_device ):
            raise BadClassType('Argument is not a Virpil_device: ' + str(type(device)) )
        
        self._devices[name] = device
        
        #thread = threading.Thread( device.listen() )
        #thread.start()
        #self._threads.append( thread )
    
    def loop(self):
        try:
            while True:
                for name, device in self._devices.items():
                
                    for led in device._slave.led_names:
                        if device.update:
                            device.setSlaveLed( led, getRandomColor() )
                    
                    for led in device.led_names:
                        if device.update:
                            device.setLed( led, getRandomColor() )
                
                    if device.update:
                        print( 'Activate ' + name )
                        device.sendFeatureReport(master=True, slave=True)
                    
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nKeyboardInterrupted")
            exit()
        except:
            print(traceback.format_exc())






try:
    devHandle = Multi_Device_Handler()

    devHandle.addDevice('VPC_left',
            Virpil_Alpha_Prime(
                    vendor_id=0x3344, product_id=0x0137,
                    slave=Virpil_Control_Panel_2(),
                    )
            )
    devHandle.addDevice('VPC_right',
            Virpil_Alpha_Prime(
                    vendor_id=0x3344, product_id=0xC138,
                    slave=Virpil_Control_Panel_1(),
                    )
            )

    devHandle.loop()

except KeyboardInterrupt:
    print("\nKeyboardInterrupted")
    exit()
except:
    print(traceback.format_exc())