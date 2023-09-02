import socket
import threading

import traceback



KILL_SERVER = bytes( [0xff] )

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
        
        print('Client sending data')
        self._socket.send(data)
    
    def serverListen(self):
        if not self._is_server:
            raise Exception('Not a socket server instance')
        
        print('Server listening on port ' + str(self.getPort()) )
        
        # Listen only one client at a time.
        self._socket.listen(1)
        
        running = True
        while running:
            (client, address) = self._socket.accept()
            data = bytes( client.recv( self._buffer_size ) )
        
            if data != '':
                print('Receiving data on port ' + str(self.getPort()) + ':', end='')
                print( data )
            
            # Stop server
            if data == KILL_SERVER:
                print('Stop data reveived; killing server ' + str(self.getPort()) )
                running = False
            
            data = ''
    
    
    def _initServer(self, port=False):
        """
        Create socket, and eventually change port for the next Virpil_master
        instance.
        """
        
        if not port:
            port = ConnectHandle._port
        self._port = port
        
        print( 'Init server on port ' + str(port) )
        
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # 38 uint8 buffer
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self._buffer_size)
            
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
            print('Closing socket')
            self._socket.close()

