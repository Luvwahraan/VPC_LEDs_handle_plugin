import hid
import time
import random

import traceback



"""
    I use Virpil HOSAS, with control panels:
        left Constellation Alpha Prime, with Control Panel #2 in slave.
        right Constellation Alpha Prime, with Control Panel #1 in slave.
"""


class BadClassType(Exception):
    pass
class WarnVirpilSlaveType(Exception):
    pass
class LEDValueRange(Exception):
    pass
class LEDBankExcept(Exception):
    pass



class Virpil_device:
    """
    Empty virpil device class.
    Is not intended to be directly instanced.
    
    
    Attributes
    ----------
    _slave : Virpil_slave
        Virpil_device child, without hid handle
    _is_master : bool
        device has slave
    _is_slave : bool
        device is slave
    _led_bank : uint8 list
        contains device LEDs informations
        
    Methods
    -------
     createLedBank(buttonNames, value)
        Create _led_bank dict, with LED names as keys.
        Default value is LED off (black)
    setAllLeds(value)
        Set all LED with value.
    
    """
    
    def __init__(self):
        self._slave = False
        self._is_slave = False
        self._is_master = False
        self._led_bank = { }
        self._hid_cmd = 0
    
    def getCmd(self):
        return self._hid_cmd
    
    def setCmd(self, cmd):
        self._hid_cmd = cmd
    
    def setThisMaster(self):
        self._is_slave = False
        self._master = True

    def setThisSlave(self):
        self._is_slave = True
        self._master = False
    
    def getLedBank(self):
        return self._led_bank
    
    def createLedBank(self, buttonNames, value=0b11000000):
        """
            Fill all led_bank with one value.
            Need a list, to make dictionnary.
            Value is optionnal (turn off LEDs by default).
        """
        
        # Do not try to create an empty led_bank
        if len(buttonNames) < 1:
            raise Exception('Can’t create empty led_bank array.')
        
        # Raise exception if not valid
        self.checkLedValue(value)
        
        # Need a list
        if isinstance(buttonNames, list):
            for name in buttonNames:
                self._led_bank[name] = value
        else:
            print( buttonNames )
            raise LEDBankExcept('buttonNames' + str( type(buttonNames) ) + 'list arg not valid.')
    
    def checkLedValue(self, value):
        if 0 <= value and value <= 255: # between 0b00000000 and 0b11111111
            return
        else:
            raise LEDValueRange('LED value is not in 64-255 range.')

    
    def setLed(self, btnName, value):
        """ Set one led value. """
        self.checkLedValue(value)
        try:
            self._led_bank[btnName] = value
        except:
            return False
    
    def getLedValues(self):
        """
        Returns a 38 uint8 list from _led_bank values.
        """
        return list(self.getLedBank().values() )
    
    
    def setAllLeds(self, value):
        self.createLedBank( list(self._led_bank.keys()), value )


class Virpil_master(Virpil_device):
    """
    Virppil device that is not a slave.
    Need HID path to work, but can search it with vendor_id and product_id.
    
    TODO:
        Validate path.
    
    
    Attributes
    ----------
    _hidraw : hid.device()
        hidapi
    
    Methods
    -------
    getPathByIds(vendor_id, product_id)
        Searches hid path, by vip/pid.
    setSlaveLeds(value)
        Sets all LED for slave.
        Value is uint8 − 64 to 255 are valid colors
    activate()
        Makes hid feature_report and send to device
    """
    
    def _initHID(self):
        self._hidraw = hid.device()
        self._hidraw.open_path( self._path )
        self._hidraw.set_nonblocking(1)
    
    def __init__(self, vendor_id=False, product_id=False, path=False, slave=False):
        # Need path or vendor_id/product_id couple.
        # slave is optionnal Virpil_slave
        
        Virpil_device.__init__(self)
        
        if path != False: 
            # Doesnt verify if path is valid.
            self._path = path
        elif vendor_id != False and product_id != False:
            self._path =  self.getPathByIds(vendor_id, product_id)
        else:
            raise Exception('Missing usb hid args.')
            
        if slave != False:
            self.setSlave(slave)
        
        self._initHID()
    
    
    def getPathByIds(self, vendor_id, product_id):
        """
        Works fine with my config. Maybe it’s bad…
        """
        
        hid_device = hid.enumerate(vendor_id, product_id)
        return hid_device[len(hid_device)-1]['path']
    
    
    def setSlave(self, slave):
        """
        Need a Virpil_slave, but should works with generic Virpil_device,
            by setting _hid_cmd and _led_bank manually.
        """
        
        if not isinstance( slave, Virpil_device ):
            raise BadClassType('Argument is not a Virpil_device: ' + str(type(slave)) )
        elif not isinstance( slave, Virpil_slave ):
            raise WarnVirpilSlaveType('Be aware: argument is not a Virpil_slave.' )
        self._slave = slave
    
    def setAllMasterLeds(self, value):
        Virpil_device.setAllLeds(self, value)
    
    def setAllSlaveLeds(self, value):
        self._slave.setAllLeds(value)
    
    def setSlaveLed(self, btnName, value):
        self._slave.setLed(btnName, value)
    
    def setAllLeds(self, value):
        self.setAllMasterLeds(value)
        self.setAllSlaveLeds(value)
    
    # TO DO: separate master and slave
    def activate(self):
        # Construct feature_report with command, leds and end.
        
        # For master
        master_feature_report = [0x2, self.getCmd(), 0x00, 0x00, 0x00] + self.getLedValues() + [0xF0]
        
        # # … and slave
        slave_feature_report = [0x2, self._slave.getCmd(), 0x00, 0x00, 0x00] + self._slave.getLedValues() + [0xF0]
        
        # Then activate LEDs on both.
        if self._hidraw.send_feature_report( master_feature_report ) == -1:
            print( master_feature_report )
            raise Exception( self._hidraw.error() )
        if self._hidraw.send_feature_report( slave_feature_report ) == -1:
            print( slave_feature_report )
            raise Exception( self._hidraw.error() )



class Virpil_slave(Virpil_device):
    """
    Virpil device intended to be slaved into a Virpil_master class.
    Does not need vendor_id/product_id or _hid_cmd, since the master handle hidapi.
    """
    
    def __init__(self):
        Virpil_device.__init__(self)
        self.setThisSlave()
        self.setCmd(0x67) # SLAVE_BOARD


class Virpil_Alpha_Prime(Virpil_master):
    """ Virpil Constellation Alpha Prime class.
    Register 9 LEDs : 5 on side and 4 on top.
    
    https://virpil-controls.eu/vpc-constellation-alpha-prime-l.html
    https://virpil-controls.eu/vpc-constellation-alpha-prime-r.html
    """
    
    def __init__(self, vendor_id=0, product_id=0, slave=0):
        self.led_names = [
                'S1', 'S2', 'S3', 'S4', 'S5',
                'H1', 'H2', 'H3', 'H4' ]
        Virpil_master.__init__(self, vendor_id=vendor_id, product_id=product_id, slave=slave)
        Virpil_device.createLedBank(self, self.led_names)
        self.setCmd(0x68) # EXTRA_LEDS


class Virpil_Control_Panel_1(Virpil_slave):
    """ VPC Control Panel - #1 class
    Register 12 LEDs : 6 on top buttons and 6 on left bottom buttons.
    
    https://virpil-controls.eu/vpc-control-panel-1.html
    """
    
    def __init__(self):
        self.led_names = [
                'B10', 'B11', 'B12', 'B7', 'B8',
                'B9', 'B6', 'B4', 'B2', 'B5', 'B3', 'B1' ]
        Virpil_slave.__init__(self)
        Virpil_device.createLedBank(self, self.led_names)


class Virpil_Control_Panel_2(Virpil_slave):
    """ VPC Control Panel - #2 class
    Register 17 LEDs : 4 on top buttons, 7 on gears, and 6 more on right bottom buttons.
    
    https://virpil-controls.eu/vpc-control-panel-2.html
    """
    
    def __init__(self):
        self.led_names = [
                'B2', 'B1', 'B4', 'B3',
                #'GUp', 'GMiddle', 'GLeft', 'G1', 'G2', 'G3', 'GRight', # I don't know how to call theses LED. /-:
                'FlapsTop', 'FlapsLeft', 'GearLeft', 'GearFront', 'GearRight', 'FlapsRight',
                'B10', 'B8', 'B6', 'B9', 'B7', 'B5' ]
        Virpil_slave.__init__(self)
        Virpil_device.createLedBank(self, self.led_names)



def getRandomColor():
    return random.randrange(65, 256)


class Multi_Device_Handler:
    """
    Handle multiple Virpil_device object.
    
    
    Attributes
    ----------
    _device
        dictionnary: { deviceName: {device: Virpil_device, update: bool }
        Setting update to True will cause update at next iteration
    
    Methods
    -------
    
    
    """

    def __init__(self):
        self._device = {} 
        self._threads = []
    
    def addDevice(self, name, device):
        if not isinstance( device, Virpil_device ):
            raise BadClassType('Argument is not a Virpil_device: ' + str(type(device)) )
        self._device[name] = { 'device': device, 'update': True }
    
    def _run_thread(self, function, *args, **kwargs):
        pass
    
    def loop(self):
        try:
            while 1:
                for name, device_dict in self._device.items():
                    for led in device_dict['device']._slave.led_names:
                        if device_dict['update']:
                            device_dict['device'].setSlaveLed( led, getRandomColor() )
                            print('Changing '+led+' for '+name+'’s slave')
                    device_dict['device'].activate()
                time.sleep(10)
            
        except KeyboardInterrupt:
            print("\nKeyboardInterrupted")
            exit()
        except:
            print(traceback.format_exc())






try:
    devHandle = Multi_Device_Handler()

    devHandle.addDevice('VPC_left',
            Virpil_Alpha_Prime(vendor_id=0x3344, product_id=0x0137, slave=Virpil_Control_Panel_2() ) )
    devHandle.addDevice('VPC_right',
            Virpil_Alpha_Prime(vendor_id=0x3344, product_id=0xC138, slave=Virpil_Control_Panel_1() ) )

    devHandle.loop()

except KeyboardInterrupt:
    print("\nKeyboardInterrupted")
    exit()
except:
    print(traceback.format_exc())