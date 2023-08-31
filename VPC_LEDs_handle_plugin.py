import hid
import numpy
import time

import traceback



0x00 = 0x0




class BadClassType(Exception):
    pass
class WarnVirpilSlaveType(Exception):
    pass
class LEDValueRange(Exception):
    pass

class Virpil_device:
    """
    Empty virpil device class.
    Is not intended to be instanced.
    
    Attributes
    ----------
    _slave : Virpil_slave
        Virpil_device child, without hid handle
    _is_master : bool
        device has slave
    _is_slave : bool
        device is slave
    _led_bank : numpy.uint8 list
        contains device LEDs informations
    """
    
    def __init__():
        self._slave = False
        self._is_slave = False
        self._is_master = False
        self._led_bank = []
        self.setCmd( slave_feature_report )
    
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
    
    def createLedBank(self, nb, value=0b11000000):
        # Do not try to create an empty led_bank
        if nb < 1:
            raise Exception('Can’t create empty led_bank array.')
        self._led_bank = numpy.full( nb, 0, dtype=numpy.uint8)
    
    def checkLedValue(self, value):
        if 0 <= value and value <= 255: # between 0b00000000 and 0b11111111
            return
        else:
            raise LEDValueRange('LED value is not in 64-255 range.')

    
    def setLed(self, nb, value):
        """ Set one led value. """
        self.checkLedValue(value)
        try:
            self._led_bank[nb] = value
        except:
            return False
        
        return self._led_bank
    
    def setAllLeds(self, value):
        self.checkLedValue(value)
        self._led_bank = numpy.full( len(self._led_bank), value, dtype=numpy.uint8)


class Virpil_master(Virpil_device):
    """
    Virppil device that is not a slave.
    Need HID path to work, but can search it with vendor_id and product_id.
    
    TODO:
        Validate path.
    """
    
    def _initHID(self):
        self._hidraw = hid.device()
        self._hidraw.open_path( self._path )
        self._hidraw.set_nonblocking(1)
    
    def __init__(self, vendor_id=False, product_id=False, path=False, slave=False):
        # Need path or vendor_id/product_id couple.
        # slave is optionnal Virpil_slave
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
        Works fine with my config.
        """
        
        hid_device = hid.enumerate(vendor_id, product_id)
        return hid_device[len(hid_device)-1]['path']
    
    
    def setSlave(self, slave):
        """
        Need a Virpil_slave, but could works with generic Virpil_device.
        """
        
        if not isinstance( slave, Virpil_device ):
            raise BadClassType('Argument is not a Virpil_device: ' + str(type(slave)) )
        elif not isinstance( slave, Virpil_slave ):
            raise IamAPotato('Potato!')
            raise WarnVirpilSlaveType('Be aware: argument is not a Virpil_slave.' )
        self._slave = slave
    
    def setAllMasterLeds(self, value):
        Virpil_device.setAllLeds(self, value)
    
    def setAllSlaveLeds(self, value):
        self._slave.setAllLeds(value)
    
    def setAllLeds(self, value):
        self.setAllMasterLeds(value)
        self.setAllSlaveLeds(value)
    
    def activate(self):
        # Construct feature_report with command, leds and end.
        
        # For master
        master_feature_report = numpy.insert( self._led_bank, 0,
                numpy.array( [0x2, self.getCmd(), 0x00, 0x00, 0x00], dtype=numpy.uint8 ) )
        master_feature_report = numpy.append( master_feature_report, numpy.array([0xF0], dtype=numpy.uint8) )
        
        # … and slave
        slave_feature_report = numpy.insert( self._slave._led_bank, 0,
                numpy.array( [0x2, self._slave.getCmd(), 0x00, 0x00, 0x00], dtype=numpy.uint8 ) )
        slave_feature_report = numpy.append( slave_feature_report, numpy.array([0xF0], dtype=numpy.uint8) )
        
        # Then activate LEDs on both.
        if self._hidraw.send_feature_report( master_feature_report ) == -1:
            raise Exception( self._hidraw.error() )
        if self._hidraw.send_feature_report( slave_feature_report ) == -1:
            raise Exception( self._hidraw.error() )



class Virpil_slave(Virpil_device):
    """
    Virppil device intended to be slaved into a Virpil_master class.
    Does not need vendor_id/product_id, since the master handle USB.
    """
    
    _hid_cmd = 0x67 # SLAVE_BOARD
    
    def __init__(self):
        self.setThisSlave()


class Virpil_Alpha_Prime(Virpil_master):
    """
    Virpil Constellation Alpha Prime class.
    Register 9 LEDs.
    
    https://virpil-controls.eu/vpc-constellation-alpha-prime-l.html
    https://virpil-controls.eu/vpc-constellation-alpha-prime-r.html
    """
    
    _hid_cmd = 0x68 # EXTRA_LEDS
    
    def __init__(self, vendor_id=0, product_id=0, slave=0):
        Virpil_master.__init__(self, vendor_id=vendor_id, product_id=product_id, slave=slave)
        Virpil_device.createLedBank(self, 9)


class Virpil_Control_Panel_1(Virpil_slave):
    """
    VPC Control Panel - #1 class
    Register 12 LEDs
    https://virpil-controls.eu/vpc-control-panel-1.html
    """
    
    def __init__(self):
        Virpil_device.createLedBank(self, 12)


class Virpil_Control_Panel_2(Virpil_slave):
    """
    VPC Control Panel - #2 class
    Register 17 LEDs
    
    https://virpil-controls.eu/vpc-control-panel-2.html
    """
    
    def __init__(self):
        Virpil_device.createLedBank(self, 17)



VPC_left = Virpil_Alpha_Prime(vendor_id=0x3344, product_id=0x0137, slave=Virpil_Control_Panel_2() )
VPC_right = Virpil_Alpha_Prime(vendor_id=0x3344, product_id=0xC138, slave=Virpil_Control_Panel_1() )

try:
    colorL = numpy.uint8(65) 
    colorR = numpy.uint8(255)
    while 1:
        # Set master and slave LED colors.
        VPC_left.setAllMasterLeds(colorL)
        VPC_left.setAllSlaveLeds(colorL)
        
        # Or both.
        VPC_right.setAllLeds(colorR)
    
        VPC_left.activate()
        VPC_right.activate()
        
        # Set all colors in range.
        colorL = (colorL + 1) % 255
        colorR = (colorR - 1) % 255
        
        time.sleep(0.3)
except KeyboardInterrupt:
    exit()
except:
    print(traceback.format_exc())