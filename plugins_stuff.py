import socket
import threading
import sys
import traceback



try:
    import gremlin
    from gremlin.user_plugin import *
    import logging
except:
    pass

def dprint( string ):
    if 'gremlin' not in sys.modules:
        print( string )
    else:
        gremlin.util.log( string )

KILL_SERVER = 0xff
EXTRA_LEDS = 0x68
SLAVE_BOARD = 0x67

TURN_OFF = [0, 0, 0, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 0xf0]


class ConnectHandle():
    _port = 14517
    _buffer_size = 38*8
    
    
    def clientSend(self, data):
        if not self._is_client:
            raise Exception('Not a socket client instance')

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect( ('localhost', self._port) )
        
        if socket == False:
            raise Exception('Something goes wrong with socket.connect')
        
        #dprint('Client sending data')
        self._socket.send( data )
    
    def serverListen(self, callback=False):
        if not self._is_server:
            raise Exception('Not a socket server instance')
        
        dprint('Server listening on port ' + str(self.getPort()) )
        
        # Listen only one client at a time.
        self._socket.listen(1)
        
        running = True
        while running:
            (client, address) = self._socket.accept()
            #dprint('New client ' +str(address ) )
            data = bytes( client.recv( self._buffer_size ) )
            
        
            if data != '':
                #print('Receiving data on port ' + str(self.getPort()) + ':', end='')
                #print( data )
                pass
            
            # Stop server
            if data == bytes( [KILL_SERVER] ):
                print('Stop data reveived; killing server ' + str(self.getPort()) )
                running = False
                
                # Joystick LEDs off
                data = [0x02, 0x68] + TURN_OFF
                #print( 'dataMaster:' + str(data) )
                callback(master=True, featureReport=data )
                
                # Board LEDs off
                data = [0x02, 0x67] + TURN_OFF
                #print( 'dataSlave:' + str(data) )
                callback(slave=True, featureReport=data )
                
                return
                
            if callback == False:
                raise Exception('No callback: server '+str(self.getPort())+' is useless')
            
            #if data[1] == EXTRA_LEDS:
            #    print('Constellation Alpha Grip LEDS')
            #    pass
            #elif data[1] == SLAVE_BOARD:
            #    print('Slave board LEDs')
            #    pass
            #else:
            #    print( 'Data unknown' )
            
            if running:
                callback( master=True, featureReport=data )
            data = ''
    
    
    def _initServer(self, port=False):
        """
        Create socket, and eventually change port for the next Virpil_master
        instance.
        """
        
        if not port:
            port = ConnectHandle._port
        self._port = port
        
        #dprint( 'Init server on port ' + str(port) )
        
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 38 uint8 buffer
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self._buffer_size)
            
            self._socket.bind( ('localhost', self._port) )
        except:
             dprint(traceback.format_exc())
        
        if self._port == ConnectHandle._port:
            ConnectHandle._port += 1
        
    
    def _initClient(self, port=False):
        """
        Create socket, and eventually change port for the next Virpil_master
        instance.
        """
        
        if not port:
            port = ConnectHandle._port
        self._port = port
        
        dprint( 'Init client on port ' + str(port) )
        
        if self._port == ConnectHandle._port:
            ConnectHandle._port += 1
    
    def getPort(self):
        return self._port
        
    
    def isServer(self):
        return self._is_server
    
    def isClient(self):
        return self._is_client
        
    
    def __init__(self, server=False, client=False, port=False):
        if server and client:
            raise Exception('Cannot be both client and server.')
        
        self._is_server = bool(server)
        self._is_client = bool(client)
        
        if server:
            self._initServer(port)
        if client:
            self._initClient(port)
    
    def __del__(self):
        if self._is_client or self._is_server :
            dprint('Closing socket')
            self._socket.close()






colorMap = {
      'off': 0b10000000,
      'white-dim': 0b10010101,
      'white-medium': 0b10101010,
      'white-bright': 0b10111111,
      'white': 0b10101010,
      'red-dim': 0b10000001,
      'red-medium': 0b10000010,
      'red-bright': 0b10000011,
      'red': 0b10000010,
      'green-dim': 0b10000100,
      'green-medium': 0b10001000,
      'green-bright': 0b10001100,
      'green': 0b10001000,
      'blue-dim': 0b10010000,
      'blue-medium': 0b10100000,
      'blue-bright': 0b10110000,
      'blue': 0b10100000,
      'yellow-dim': 0b10000101,
      'yellow-medium': 0b10001010,
      'yellow-bright': 0b10001111,
      'yellow': 0b10001010,
      'magenta-dim': 0b10010001,
      'magenta-medium': 0b10100010,
      'magenta-bright': 0b10110011,
      'magenta': 0b10100010,
      'cyan-dim': 0b10010100,
      'cyan-medium': 0b10101000,
      'cyan-bright': 0b10111100,
      'cyan': 0b10101000,
      'orange': 0b10001011,
      'salmon': 0b10011011,
      'red-orange': 0b10000111,
      'red-pink': 0b10010011,
      'pink': 0b10100111,
      'purple': 0b10110010,
      'indigo': 0b10100001,
      'light-blue': 0b10111010,
      'lime-green': 0b10001110
  }

led_names = {
        grip_leds: [ 'S1', 'S2', 'S3', 'S4', 'S5', 'H1', 'H2', 'H3', 'H4' ],
        panel1_leds: [ 'B10', 'B11', 'B12', 'B7', 'B8', 'B9', 'B6', 'B4', 'B2', 'B5', 'B3', 'B1' ],
        panel2_leds [
            'B2', 'B1', 'B4', 'B3',
            'GearUpNose', 'GearIndicator', 'GearUpLeft',
            'GearDownLeft', 'GearDownNose', 'GearDownRight',
            'GearUpRight',
            'B10', 'B8', 'B6', 'B9', 'B7', 'B5' ]
    }

class Button():
    def _validatedSide(side):
        if side == 'left' or side == 'right':
            return side
        else:
            raise Exception( "Side has to be 'left' or 'right', not '{v}'".format(v=side) )
    
    def _validatedType(btype):
        if btype == 'toggle' or btype == 'hold' or btype == 'timed':
            return btype
        else:
            raise Exception( "btype has to be: toggle, hold, timed. Not '{v}'".format(v=side) )
        
    
    def addLED( led ):
        if not isinstance(led, LED):
            raise Exception( 'Bad type: ' + str(led) )
        
        self._led[ led.name ] = led
    __init__(self, nb, side, btype='togle' description=''):
        if ( is_integer( nb ) and nb > 0 ):
            self.number = nb
        else:
            raise Exception( 'Button number has to be a positive integer; '{v}' is not.'.format(v=nb) )
        
        self.side = _validatedSide(side)
        self.btype = _validatedType(btype)
        
        if description != '':
            self.description = str(description)
        
        # Need a list, but LED has to be unique.
        _led = {}
    

class LED():
    def _validatedSide(side):
        if side == 'left' or side == 'right':
            return side
        else:
            raise Exception( "Side has to be 'left' or 'right', not '{v}'".format(v=side) )
        
    
    def changeColor(self, colorMap[ self.color ]):
        # Should throw an error if doesn't exist
        self.color = colorMap[ colorName ]
        
        self.colorName = colorName
        
    
    __init__(self, name, side, colorName, device, active=False):
    """
        name
            see led_names list
            
        side
            left or right
            
        colorName
            see colorMap dict
            
        device
            what device the led is on: master or slave
            
        active (optional)
            True when LED on, else False
    """
        self.side = _validatedSide(side)
        self.device = device
        self.active = active
        
        changeColor(colorName)
        
    