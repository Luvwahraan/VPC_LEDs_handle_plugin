import hid
import time
import random
import socket
import threading
import traceback

from evdev import list_devices, InputDevice

from data import LedNames, ColorMap, LedBank
from plugins_stuff import LED as LED

class BadClassType(Exception):
    pass
class WarnVirpilSlaveType(Exception):
    pass
class LEDValueRange(Exception):
    pass
class LEDBankExcept(Exception):
    pass
class NoConnectionError(Exception):
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
     setLedBank(LedBank)
        Set _led_bank.
        See LedBank object
    setAllLeds(value)
        Set all LED with value.

    """
    
    def __init__(self):
        self._slave = False
        self._is_slave = False
        self._is_master = False
        self._led_bank = LedNames.getBank()
        self._hid_cmd = 0
        self._debug = True
        
        self.update = True

    def setDebug(self, value=True):
        self._debug = value
        if (self._debug):
            print("DEBUG mode.")
        else:
            print("Disabled DEBUG mode.")
    
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

    def getDeviceType(self):
        if self._is_slave:
            return 'slave'
        else:
            return 'master'
    
    def getLedBank(self):
        return self._led_bank

    def getLedNames(self):
        return self._led_bank.getNames()
    
    def setLedBank(self, led_bank):
        if not isinstance(led_bank, LedBank):
            raise Exception("{s} is not a LedBank object.".format(s=led_bank) )
        if self._debug:
            print("  Creating LedBank:\n    ", end='')
            for led in led_bank.getNames():
                print(led, end=' ')
            print('')

        self._led_bank = led_bank
    
    def checkLedValue(self, value):
        if isinstance(value, str):
            if not value in ColorMap.colors:
                raise LEDValueRange('LED value ' + value + 'doesnt exist.')
            return
        elif isinstance(value, int):
            if 0 <= value and value <= 255: # between 0b00000000 and 0b11111111
                return
            else:
                raise LEDValueRange('LED value is not in 0-255 range.')
        
    
    def setLed(self, btnName, value):
        """
        Set one led value.
        See data.ColorMap for values.
        """
        self.checkLedValue(value)
        try:
            self._led_bank.setLed(btnName, value)
            if self._debug: print( 'Setted ' + btnName + ' to ' + str(value) )
        except:
            if self._debug: print( 'No LED setted. ' + traceback.format_exc() )
            return False
        
    
    def getLedValues(self):
        """
        Returns a 32 list from _led_bank values.
        """
        
        # Create list
        led_list = self._led_bank.getValues()
        
        # Finish list if too short
        while len( led_list ) < 32:
            led_list.append(0)
        
        return list(led_list)
        
    
    def setAllLeds(self, value='off'):
        self._led_bank.setAllLeds(value)
    


class Virpil_slave(Virpil_device):
    """
    Virpil device intended to be slaved into a Virpil_master class.
    Does not need vendor_id/product_id or _hid_cmd, since the master handle hidapi.
    """
    
    def __init__(self):
        Virpil_device.__init__(self)
        self.setThisSlave()
        
    


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
        Value is uint8 - 64 to 255 are valid colors
    sendFeatureReport()
        Makes hid feature_report and send to device
    """
    
    
    
    def _initHID(self):
        """
        Create hid stuff in order to communicate with device.
        """
        self._hidraw = hid.device()
        self._hidraw.open_path( self._path )
        self._hidraw.set_nonblocking(1)
        
    
    
    def __del__(self):
        # USB hid raw
        if self._hidraw != False:
            self._hidraw.close()

    def searchDevice(self):
        for path in list_devices():
            dev = InputDevice(path)
            if dev.info.vendor == self._vendor_id and dev.info.product == self._product_id:
                return dev
        else:
            raise RuntimeError("No device found.")
        
    
    def __init__(self, vendor_id=False, product_id=False, slave=False ):
        """
        Need path or vendor_id/product_id couple.
        slave is optionnal Virpil_slave
        
        This class can optionnaly starts client or server connection, but not both,
        in order to send or receive data to manage: pass server or client arg
        to True, with or without port.
        """
        
        Virpil_device.__init__(self)
        
        self._featureReports = { 'master': [], 'slave': [] }
        
        if vendor_id != False and product_id != False:
            self._vendor_id = vendor_id
            self._product_id = product_id
            self._path =  self.getPathByIds(vendor_id, product_id)
        else:
            raise Exception('Missing usb hid args.')
            
        if slave != False:
            self.setSlave(slave)

        self._hidraw = False
        self._initHID()

        self.device = self.searchDevice()
        self._valid = True

    def __del__(self):
        try:
            if self._valid:
                self.activeAll('off')
        except:
            pass
        pass
    
    def getPathByIds(self, vendor_id, product_id):
        """
        Works fine with my config. Maybe it's bad...
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

    def getSlaveLedNames(self):
        return self._slave.getLedNames()
    
    def setAllMasterLeds(self, value='off'):
        """
        Set all LED on master to a value.
        Do not activate led on device (see activeMaster methods).
        """
        Virpil_device.setAllLeds(self, value)
    
    def setAllSlaveLeds(self, value='off'):
        """
        Set all LED on slave to a value.
        Do not activate led on device (see activeSlave methods).
        """
        self._slave.setAllLeds(value)
    
    def setSlaveLed(self, btnName, value='off'):
        """
        Set specific led on slave to a value.
        Do not activate led on device (see activeSlave methods).
        """
        self._slave.setLed(btnName, value)
    
    def setAllLeds(self, value='off'):
        """
        Set leds to a value for master and slave.
        Do not activate led on device (see active* methods).
        """
        self.setAllMasterLeds(value)
        self.setAllSlaveLeds(value)

    def activeLed(self, btnName, value='off'):
        """
        Search a LED by his button name, then activate.
        """
        device = self.searchLed(btnName)

        if isinstance(device, Virpil_slave):
            self.setSlaveLed(btnName, value)
            self.activeSlave()
        elif isinstance(device, Virpil_master):
            self.setLed(btnName, value)
            self.active()
        else:
            if self._debug: print( 'Unknow device ' + str(type(device) ) )
        
        return
        
        if device != False:
            if device._is_slave:
                self.setSlaveLed(btnName, value)
                self.activeSlave()
            else:
                self.setLed(btnName, value)
                self.active()

    def activeAllLeds(self, value='off'):
        """
        Set all leds to a value (defaut off), for master and slave,
        then activate on device.
        """
        self.setAllMasterLeds(value)
        self.setAllSlaveLeds(value)
        self.active()
        self.activeSlave()

    def searchLed(self, btnName):
        """
        Search if there is a led on btnName, and in wich device
        (master or slave).
        Return device or False.
        """
        for led in self.getLedNames():
            if led == btnName:
                return self
        for led in self._slave.getLedNames():
            if led == btnName:
                return self._slave
            
        
    def constructMasterFeature(self):
        self._featureReports['master'] = [0x2, self.getCmd(), 0x00, 0x00, 0x00] + self.getLedValues() + [0xF0]
        self.update = True
    
    def constructSlaveFeature(self):
        self._featureReports['slave'] = [0x2, self._slave.getCmd(), 0x00, 0x00, 0x00] + self._slave.getLedValues() + [0xF0]
        self._slave.update = True
    
    def activeMaster(self, featureReport=False):
        self.sendFeatureReport(True, False, featureReport)
    def active(self, featureReport=False):
        self.sendFeatureReport(True, False, featureReport)
    
    def activeSlave(self, featureReport=False):
        self.sendFeatureReport(False, True, featureReport)

    def activeAll(self, featureReport=False):
        self.sendFeatureReport(True, False, featureReport)
        self.sendFeatureReport(False, True, featureReport)

    def sendFeatureReport(self, master=False, slave=False, featureReport=False):
        masterFeature = []
        slaveFeature = []
        
        # With featureReport in arg, we can't send both master and slave.
        if featureReport == True and ( master and slave ):
            raise Exception("Can't send both master and slave feature_report")

        if master:
            if self._debug: print( 'sending for master:', end=' ' )
        
            # Use arg featureReport, or construct with self data.
            if featureReport:
                if self._debug: print( 'Received master featureReport:', end=' ' )
                self._featureReports['master'] = featureReport
            else:
                self.constructMasterFeature()
                
            if self._hidraw.send_feature_report( self._featureReports['master'] ) == -1:
                raise Exception( self._hidraw.error() + ': ' + str(self._featureReports['master']) )
            if self._debug: print( self._featureReports['master'] )
        
        if slave:
            if self._debug: print( 'sending for slave:', end=' ' )
            
            if featureReport:
                if self._debug: print( 'Received slave featureReport:', end=' ' )
                self._featureReports['slave'] = featureReport
            else:
                self.constructSlaveFeature()
            
            if self._hidraw.send_feature_report( self._featureReports['slave'] ) == -1:
                raise Exception( self._hidraw.error() + ': ' + str(self._featureReports['slave']) )
            if self._debug: print( self._featureReports['slave'] )
        
    



class Virpil_Alpha_Prime(Virpil_master):
    """ Virpil Constellation Alpha Prime class.
    Register 9 LEDs : 5 on side and 4 on top.

    https://virpil-controls.eu/vpc-constellation-alpha-prime-l.html
    https://virpil-controls.eu/vpc-constellation-alpha-prime-r.html
    """
    
    def __init__(self, vendor_id=0, product_id=0, slave=0, server=False, client=False):
        Virpil_master.__init__(self, vendor_id=vendor_id, product_id=product_id, slave=slave)
        Virpil_device.setLedBank(self, LedNames.alpha_prime)
        self.setCmd(0x67)
        
    


class Virpil_Control_Panel_1(Virpil_slave):
    """ VPC Control Panel - #1 class
    Register 12 LEDs : 6 on top buttons and 6 on left bottom buttons.

    https://virpil-controls.eu/vpc-control-panel-1.html
    """
    
    def __init__(self):
        Virpil_slave.__init__(self)
        Virpil_device.setLedBank(self, LedNames.panel1)
        self.setCmd(0x6A)
        
    


class Virpil_Control_Panel_2(Virpil_slave):
    """ VPC Control Panel - #2 class
    Register 17 LEDs : 4 on top buttons, 7 on gears, and 6 more on right bottom buttons.

    https://virpil-controls.eu/vpc-control-panel-2.html
    """
    
    def __init__(self):
        Virpil_slave.__init__(self)
        Virpil_device.setLedBank(self, LedNames.panel2)
        self.setCmd(0x6A)
        
    
