import socket
import threading
import sys
import traceback


#KILL_SERVER = [0xfa, 0xbb, 0xaf]
KILL_SERVER = [0xff]

#TURN_OFF = [0, 0, 0, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 0xf0]
#TURN_OFF = [0, 0, 0, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80]
TURN_OFF = []
for i in range(0,35):
    TURN_OFF.append(0)

class Command():
    end =       0xf0 # end data
    kill =      0xff # stop server command
    led =       0xf9 # parsing led command
    separator = 0x01 # parsing led separator
    feature =   0x02 # full featureReport command


class ConnectHandle():
    _port = 14517
    #_buffer_size = 38 # 38 bytes
    _max_buffer_size = 128
    
    def clientSend(self, data):
        if not self._is_client:
            raise Exception('Not a socket client instance')

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect( ('localhost', self._port) )
        
        if socket == False:
            raise Exception('Something goes wrong with socket.connect')
        
        #print('Client sending data')
        self._socket.send( data )
    
    def stop(self):
        self.clientSend(bytes(KILL_SERVER))

    def sendFeatureRecord(self, data):        
        callback( master=True, featureReport=data )

    def _killServer(self):
        # Stop server
        print('Stop data reveived; killing server ' + self.getName() )
        
        if not self._stopCallback == False:
            print('There is a stop callback. Calling it.')
            self._stopCallback()
        
        self._running = False
        return

    def setName(self, name):
        if self.isServer():
            self._name = name

    def _ledHandle(self, client):
        buffer = ''
        led = ''
        colors = {}
        leds = []

        if not self._running: return
        
        # First get color value.
        color = int.from_bytes(client.recv(1))
        #print('  color found: ' + str(color) )
        
        # Continue getting data until end byte.
        color_mode = False
        while buffer != bytes([Command.end]):
            buffer = client.recv(1)
            #print( '  Recv:' + str(buffer) )

            # Comma separates leds (0x2c in ASCII)
            # So all led data we got should be a button name.
            if buffer == bytes([0x2c]):
                #print('    new button coming')
                leds.append(led)
                led = ''

            # New led command -> another color and led(s) coming
            # We need to add already known led to colors dict
            elif buffer == bytes([Command.led]):
                #print('    new color coming')
                leds.append(led)
                colors[color] = leds
                led = ''
                leds = []
                
                # Next byte is color, we get it now.
                color = int.from_bytes(client.recv(1))
                #print('    color found: ' + str(color) )
            
            # End data
            elif buffer == bytes([Command.end]):
                #print('    end leds')
                leds.append(led)
                colors[color] = leds

            # A str byte.
            else:
                #print('    str byte:'+ str(buffer) )
                led = led+buffer.decode()
        
        if self._running:
            print('Leds: ' + str(colors))
            self._ledCallback(colors)
    
    def serverListen(self,
            callback=False,
            ledCallback=False,
            stopCallback=False,
            serverName='',            
            ):
        if not self._is_server:
            raise Exception('Not a socket server instance')


        # Check callbacks
        if callback == False:
            raise Exception('No callback: server '+str(self.getPort())+' is useless')
        else:
            self._featureReportCallback = callback

        if not stopCallback == False:
            self._stopCallback = stopCallback

        if not ledCallback == False:
            self._ledCallback = ledCallback

        if not serverName == '':
            self.setName(serverName)

        print('Server ' + self.getName() +' listening on port ' + str(self.getPort()) )
        
        # Listen only one client at a time.
        self._socket.listen(1)
        
        self._running = True
        while self._running:
            (client, address) = self._socket.accept()
            #print('New client ' +str(address ) )
            data = ''
            
            #cmds = {
            #    'killserver':       [0xff],
            #    'led':              [0xf9],
            #    'featureReport':    [0x02],
            #    }
            
            # Parse commandl, then data
            #command = bytes(client.recv(1))
            command = client.recv(1)
            print("Command: "+str(command))

            if command == bytes([Command.kill]): # kill server byte
                print("Received command kill server")
                self._killServer()
                return
                
            elif command == bytes([Command.led]): # one led command: color int then led(s) str
                print("Received command led")
                self._ledHandle(client)
                continue
                
            elif command == bytes([0x02]): # first feature report byte
                print("Received command featureReport")
                # We can receive until 0xf0 byte, but we know featureReport size is 38 bytes.
                data = command + bytes( client.recv( 37 ) )
                if self._running:
                    #callback( master=True, featureReport=data )
                    self._featureReportCallback( master=True, featureReport=data )
                    
            else:
                print("Unknown command")
                #data = bytes( client.recv( self._buffer_size -1 ) )
                continue
            
        
            if data != '':
                print('Receiving data on port ' + str(self.getPort()) + ': ', end='')
                print( data )
                pass

            if callback == False:
                raise Exception('No callback: server '+str(self.getPort())+' is useless')


    def _initServer(self, port=False):
        """
        Create socket, and eventually change port for the next Virpil_master
        instance.
        """
        
        if not port:
            port = ConnectHandle._port
        self._port = port
        
        #print( 'Init server on port ' + str(port) )
        
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 38 uint8 buffer
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self._max_buffer_size)
            
            self._socket.bind( ('localhost', self._port) )
        except:
             print(traceback.format_exc())
        
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
        
        print( 'Init client on port ' + str(port) )
        
        if self._port == ConnectHandle._port:
            ConnectHandle._port += 1
    
    def getPort(self):
        return self._port
    
    def isServer(self):
        return self._is_server
    
    def isClient(self):
        return self._is_client
    
    def getName(self):
        if self.isServer():
            return self._name        
    
    def __init__(self, server=False, client=False, port=False, ledAddr=[0x67,0x6a]):        
        self._is_server = bool(server)
        self._is_client = bool(client)
        self._name = 'unknown_'+str(port)
        self._ledAddress = ledAddr
        
        if self.isServer() and self.isClient():
            raise Exception('Cannot be both client and server.')

        elif self.isServer():
            self._stopCallback = False
            self._featureReportCallback = False
            self._initServer(port)

        elif self.isClient():
            self._initClient(port)

        else:
            raise Exception('This is neither client or server.')
    
    def __del__(self):
        if self._is_client:
            print('Closing client socket')
            self._socket.close()
            
        if self._is_server :
            print('Closing server socket')
            self._socket.close()

