import time

from ConnectHandle import ConnectHandle, Command
from data import ColorMap

connectHandles = {
    'left': ConnectHandle( client=True, port=14517, ledAddr=[0x67,0x6a] ),
    'right': ConnectHandle( client=True, port=14518, ledAddr=[0x67,0x6a] )
    }

print('Full featureReport for left and right.')
left_master = [2, 103, 0, 0, 0, 254, 129, 66, 123, 148, 105, 118, 254, 66, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 240]
left_slave = [2, 106, 0, 0, 0, 64, 72, 72, 176, 174, 65, 101, 156, 84, 161, 110, 110, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 240]
right_master = [2, 103, 0, 0, 0, 113, 162, 154, 195, 124, 86, 225, 181, 133, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 240]
right_slave = [2, 106, 0, 0, 0, 132, 113, 66, 194, 132, 225, 74, 209, 124, 120, 66, 194, 191, 123, 226, 75, 130, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 240]
connectHandles['left'].clientSend( bytes(left_master) )
connectHandles['left'].clientSend( bytes(left_slave) )
connectHandles['right'].clientSend( bytes(right_master) )
connectHandles['right'].clientSend( bytes(right_slave) )

time.sleep(5)

print('Change each led in left and right panels.')
def allLeft():
    for led in ['S1', 'S2', 'S3', 'S4', 'S5', 'H1',
            'H2', 'H3', 'H4''B2', 'B1', 'B4', 'B3',
            'GearUpNose', 'GearIndicator', 'GearUpLeft',
            'GearDownLeft', 'GearDownNose', 'GearDownRight', 'GearUpRight',
            'B10', 'B8', 'B6', 'B9', 'B7', 'B5']:
        # Server command for led and color
        data = [Command.led, ColorMap.randomColor()]
        
        # then button name with led
        for char in led:
            data.append( ord(char) )
            
        # finally end data
        data.append(Command.end)
        
        connectHandles['left'].clientSend(bytes(data))

def allRight():
    for led in ['B10', 'B11', 'B12', 'B7', 'B8', 'B9', 'B6', 'B4',
            'B2', 'B5', 'B3', 'B1']:
        # Server command for led and color
        data = [Command.led, ColorMap.randomColor()]
        
        # then button name with led
        for char in led:
            data.append( ord(char) )
            
        # finally end data
        data.append(Command.end)
        
        connectHandles['right'].clientSend(bytes(data))

allLeft()
allRight()

time.sleep(5)

print('Multiple led activated simultaneously, with a color:[leds] dict.')
ldata = connectHandles['left'].ledEncode({
    ColorMap.getValue('blue-dim'): ['B1'],
    ColorMap.getValue('red-dim'): ['B2'],
    ColorMap.randomColor(): ['B3'],
    ColorMap.randomColor(): ['B4'],
    ColorMap.getValue('green-dim'): ['GearUpNose', 'GearIndicator', 'GearUpLeft',
            'GearDownLeft', 'GearDownNose', 'GearDownRight', 'GearUpRight'],
    ColorMap.randomColor(): ['B5', 'B6'],
    ColorMap.randomColor(): ['B7', 'B8'],
    ColorMap.randomColor(): ['B9', 'B10']
    })
connectHandles['left'].clientSend( bytes(ldata) )

time.sleep(5)

#connectHandles['left'].clientSend( bytes([0xfa, 0xbb, 0xaf]) )
#connectHandles['right'].clientSend( bytes([0xfa, 0xbb, 0xaf]) )

connectHandles['left'].stop()
connectHandles['right'].stop()

connectHandles['left'].stop()
connectHandles['right'].stop()

