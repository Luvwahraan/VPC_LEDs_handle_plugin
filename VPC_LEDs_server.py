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
    dictionnary: {
        deviceName: {
            device: Virpil_device,
            connection: ConnectHandle,
            threads: Thread,
            }
    }

Methods
-------


"""

    def __init__(self):
        self._devices = {}
        self._threads = {}
        threading.Thread.__init__(self)
        
    
    def addConnection(self, device_name, conn):
    '''
    device_name (str)
    conn (ConnectHandle)
    '''
        
        # Search for wanted device, and store key (name).
        found_name = False
        for name, device in self._devices.items():
            if name == device_name:
                found_name = name
        
        # Check if device exists, and adds ConnectHandle if do
        if found_name != False:
            self._devices[found_name]['connection'] = conn
        else:
            raise NoConnectionError( name + 'not found in known devices' )
    
    def addDevice(self, device_name, device, conn=False):
    '''
    Store virpil device in a dict, by name.
    
    device_name (str)
    device (Virpil_master or Virpil_slave)
    conn (optionnal ConnectHandle)
    '''
        
        if not isinstance( device, Virpil_device ):
            raise BadClassType('Argument is not a Virpil_device: ' + str(type(device)) )
        
        # Does not set connection here, in order to check it.
        self._devices[device_name] = { 'device': device, 'connection': False, 'thread': False }
        
        if conn != False:
            self.addConnection(device_name, conn)
        
        # Create threads but for masters only, and only servers
        if isinstance( device, Virpil_master ):
            if self._devices[device_name]['connection'].isServer():
                self._devices[device_name]['thread'] = threading.Thread(
                        target=self._devices[device_name]['connection'].serverListen,
                        name=device_name,
                        args=[ self._devices[device_name]['device'].sendFeatureReport ]
                        )
        
    
    def randomizeLeds(self):
        return
        while True:
            for name, device_dict in self._devices.items():
            
                for led in device_dict['device']._slave.led_names:
                    if device_dict['device'].update:
                        device_dict['device'].setSlaveLed( led, getRandomColor() )
                
                for led in device_dict['device'].led_names:
                    if device_dict['device'].update:
                        device_dict['device'].setLed( led, getRandomColor() )
            
                if device_dict['device'].update:
                    print( 'Activate ' + name )
                    device_dict['device'].sendFeatureReport(master=True, slave=True)
            
            #time.sleep( random.uniform(0.5, 30) )
            time.sleep(120)
        
    
    
    def start(self):
        # Disco thread. \o_
        main = threading.Thread( target=self.randomizeLeds, daemon=True )
        main.start()
    
        # Starting devices threads
        for name, device_dict in self._devices.items():
            device_dict['thread'].start()
        
        main.join(2)
        
        
        # Wait for server threads.
        for name, device_dict in self._devices.items():
            device_dict['thread'].join()
        
        
    





try:
    devHandle = Multi_Device_Handler()

    devHandle.addDevice('VPC_left',
            Virpil_Alpha_Prime(
                    vendor_id=0x3344, product_id=0x8137,
                    slave=Virpil_Control_Panel_2(),
                    ),
            ConnectHandle(server=True)
            )
    devHandle.addDevice('VPC_right',
            Virpil_Alpha_Prime(
                    vendor_id=0x3344, product_id=0xC138,
                    slave=Virpil_Control_Panel_1(),
                    ),
            ConnectHandle(server=True)
            )

    devHandle.start()

except KeyboardInterrupt:
    print("\nKeyboardInterrupted")
    exit(1)
except:
    print(traceback.format_exc())