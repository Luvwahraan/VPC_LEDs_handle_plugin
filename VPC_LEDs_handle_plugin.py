import gremlin
from gremlin.user_plugin import *
from plugins_stuff import *
import sys

import logging

mode_global = ModeVariable("Global", "gl")

def dprint( string ):
    if 'gremlin' not in sys.modules:
        print( string )
    else:
        gremlin.util.log( string )

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

LEFT_GUID = '{FE8A3740-140F-11EE-8003-444553540000}'
RIGHT_GUID = '{2E6F6CA0-141F-11EE-8005-444553540000}'

grip_leds = [ 'S1', 'S2', 'S3', 'S4', 'S5', 'H1', 'H2', 'H3', 'H4' ]
panel1_leds = [ 'B10', 'B11', 'B12', 'B7', 'B8', 'B9', 'B6', 'B4', 'B2', 'B5', 'B3', 'B1' ]
panel2_leds = [
        'B2', 'B1', 'B4', 'B3',
        'GearUpNose', 'GearIndicator', 'GearUpLeft',
        'GearDownLeft', 'GearDownNose', 'GearDownRight',
        'GearUpRight',
        'B10', 'B8', 'B6', 'B9', 'B7', 'B5' ]

# Periodic callback will update device setted to True
to_update = {
    'left': {'master': True, 'slave': True},
    'right': {'master': True, 'slave': True}
    }

# Timed LED list
timed_leds = []

BUTTONS = {
    'left': {
        1: {
            'left': {
                'H1': { 'color':'red', 'device': 'master', 'active': False, 'type': 'hold' },
                'H2': { 'color':'red', 'device': 'master', 'active': False, 'type': 'hold' },
                'H3': { 'color':'red', 'device': 'master', 'active': False, 'type': 'hold' },
                'H4': { 'color':'red', 'device': 'master', 'active': False, 'type': 'hold' },
            }
        },
        33: {
            'left': {
                 'B1': { 'color': 'blue-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
            },
        },
        34: {
            'left': {
                 'B2': { 'color': 'blue-dim', 'device': 'slave', 'active': False, 'type': 'timed' },
            },
        },
        72: {
            'left': {
                 'GearIndicator': { 'color': 'red-dim', 'device': 'slave', 'active': False, 'type': 'timed' },
            },
        },
        74: {
            'left': {
                'GearDownLeft': { 'color':'green-dim', 'device': 'slave', 'active': False, 'type': 'hold' },
                'GearDownNose': { 'color':'green-dim', 'device': 'slave', 'active': False, 'type': 'hold' },
                'GearDownRight': { 'color':'green-dim', 'device': 'slave', 'active': False, 'type': 'hold' },
            },
        },
        73: {
            'left': {
                'GearUpNose': { 'color':'green-dim', 'device': 'slave', 'active': False, 'type': 'hold' },
                'GearUpLeft': { 'color':'green-dim', 'device': 'slave', 'active': False, 'type': 'hold' },
                'GearUpRight': { 'color':'green-dim', 'device': 'slave', 'active': False, 'type': 'hold' },
            },
        },
        42: {
            'left': {
                 'B10': { 'color': 'red', 'device': 'slave', 'active': False, 'type': 'toggle' },
                },
        },
        37: {
            'left': {
                'B5': { 'color': 'yellow', 'device': 'slave', 'active': False, 'type': 'timed' },
            },
        },
        39: {
            'left': {
                'B7': { 'color': 'yellow', 'device': 'slave', 'active': False, 'type': 'timed' },
            },
        },
        41: {
            'left': {
                'B9': { 'color': 'yellow', 'device': 'slave', 'active': False, 'type': 'timed' },
            },
        },
    },
    'right': {                          # Physical joystick button side
        33: {                           # Physical joystick button number
            'right': {                  # LED side: self or right
                'B1': {                 # Button name on panel or grip; see list above
                    'color':'white-dim',# See colorMap{}
                    'device': 'slave',  # master or slave device
                    'active': False,    # True: led on, False led off
                    'type': 'toggle'    # toggle, hold, timed
                    },
                },
            },
        34: {
            'left': {
                'B3': {'color':'white-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
            },
            'right': {
                'B2': {'color':'white-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
                'B3': {'color':'white-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
            },
        },
        39: {
            'right': {
                'B7': {'color':'yellow-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
            },
        },
        42: {
            'right': {
                'B10': {'color':'red-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
            },
        },
        43: {
            'right': {
                'B11': {'color':'cyan-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
            },
        },
        44: {
            'right': {
                'B12': {'color':'green-dim', 'device': 'slave', 'active': False, 'type': 'toggle' },
            },
        },
    }
}


def buildReportFeature(side, slave=False ):
    data = [0x02]
    
    if slave:
        device = 'slave'
        data += [0x67, 0x00, 0x00, 0x00]
        data += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    else:
        device = 'master'
        data += [0x68, 0x00, 0x00, 0x00]
        data += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    data.append(0xf0)

    #dprint( 'Building empty for ' + device + ' ' + str(data) )
    
    # For both left and right joystick's buttons
    for btn_side in BUTTONS.keys():
        #dprint( '  list side ' + btn_side )
        
        # browse setted buttons
        for btn in BUTTONS[btn_side].keys():
            #dprint( '    button_' + str( btn ) )
            
            try:
                for led_name in BUTTONS[btn_side][btn][side]:
                    #dprint( '      led ' + led_name )
                    
                    # but only for master or slave, one at a time
                    if BUTTONS[btn_side][btn][side][led_name]['device'] == device:
                        
                        if BUTTONS[btn_side][btn][side][led_name]['active']:
                            color = colorMap[ BUTTONS[btn_side][btn][side][led_name]['color'] ]
                            #dprint( 'Coloring ' + str(color) )
                        else:
                            #dprint( 'Turning off' )
                            color = colorMap['off']
                        
                        # Searching LED number to change
                        if slave and side == 'right':
                            led_nb = panel1_leds.index( led_name ) + 5
                        elif slave and side == btn_side:
                            led_nb = panel2_leds.index( led_name ) + 5
                        else:
                            led_nb = grip_leds.index( led_name )
                        
                        #dprint( '      updating led ' + str(led_nb) )
                        data[led_nb] = color
            except:
                #dprint( traceback.format_exc() )
                pass
    
    return data

sock_clients = {
    'left': ConnectHandle( client=True, port=14517 ),
    'right': ConnectHandle( client=True, port=14518 )
    }

JDecorators = {
    'left': gremlin.input_devices.JoystickDecorator(
            "LEFT VPC AlphaP CP2",
            LEFT_GUID,
            mode_global.value ),
    'right': gremlin.input_devices.JoystickDecorator(
            "RIGHT VPC AlphaP CP1",
            RIGHT_GUID,
            mode_global.value )
    }


period = 750 # ms


@gremlin.input_devices.periodic(period / 1000)
def checkTimed():
    if len( timed_leds ) > 0:
        dprint('timed callback timer ' + str(timed_leds) )
    
    try:
        for led_nb in range( len(timed_leds) ):            
            joy_side = timed_leds[led_nb]['button_side']
            button = int(timed_leds[led_nb]['button'])
            led_side = timed_leds[led_nb]['side']
            led_name = timed_leds[led_nb]['led']
            led_dev = timed_leds[led_nb]['device']
            
            if timed_leds[led_nb]['timer'] > 0:
                timed_leds[led_nb]['timer'] -= period
            else:
                dprint("Checking BUTTONS['{s}'][{b}]['{sl}']['{l}']".format(
                        b=button,s=joy_side,l=led_name,sl=led_side) )
                dprint( BUTTONS['left'][37]['left']['B5'] )
                BUTTONS[joy_side][button][led_side][led_name]['active'] = False
                to_update[led_side][led_dev] = True
                del( timed_leds[led_nb] )
        
    except:
        dprint( traceback.format_exc() )
        pass
    

@gremlin.input_devices.periodic(period / 3000)
def checkUpdates():
    #dprint('Periodic callback' + str(to_update) )
    
    for side in to_update.keys():
        ThisJoy = JDecorators[side]
        
        for device in to_update[side].keys():
        
            # Update buttons who have to
            if to_update[side][device]:
                dprint('Periodic callback update: ' + side + ' ' + device )
                
                if device == 'slave':
                    slave_device = True
                else:
                    slave_device = False
                
                try:
                    #dprint('Try to build data for ' + device)
                    report_feature = buildReportFeature(side, slave=slave_device)
                    
                    #dprint('Sending feature for ' + side + ' ' + device + ':' + str(report_feature) + ' on port ' + str( sock_clients[side].getPort() ) )
                    sock_clients[side].clientSend( bytes(report_feature) )
                    
                    # We don't need to do this until next update
                    to_update[side][device] = False
                except:
                    #dprint( traceback.format_exc() )
                    pass
            
        
    


LJoy = JDecorators['left']
RJoy = JDecorators['right']


def generateButtonEvents():
    generated = ''
    generatedDict = {
        'header': '',
        'comment': '',
        'pressed_event': '',
        'pressed': '',
        'released_event': '',
        'released': '',
    }
    
    for joy_side in ['left','right']:
        thisJoy = ''
        if joy_side == 'left':
            thisJoy = 'LJoy'
        elif joy_side == 'right':
            thisJoy = 'RJoy'
    
        for btn in BUTTONS[joy_side].keys():
            generatedDict['header'] = "\n\n@{j}.button({nb})\n".format(j=thisJoy, nb=btn)
            generatedDict['header'] += "def handleButton( event, joy ):\n    btn = {nb}".format(nb=btn)
            
            generatedDebug = "        dprint( 'Button ' + str(btn) + ' pushed' )\n        "

            
            for led_side in BUTTONS[joy_side][btn].keys():
                generatedDict['pressed_event'] = ''
                generatedDict['pressed'] = ''
                generatedDict['released_event'] = ''
                generatedDict['released'] = ''
                for led_name in BUTTONS[joy_side][btn][led_side].keys():
                    generatedDict['comment'] = ''
                    
                    device = BUTTONS[joy_side][btn][led_side][led_name]['device']
                    
                    # Replace colorname by value
                    color = colorMap[ BUTTONS[joy_side][btn][led_side][led_name]['color'] ]
                    
                    btype = BUTTONS[joy_side][btn][led_side][led_name]['type']
                    generatedDict['comment'] = " # {t} button\n".format(t=btype)
                        
                    button_led = "BUTTONS['{js}'][btn]['{side}']['{led}']".format(
                            js=joy_side, led=led_name, side=led_side)
                    
                    value = "BUTTONS['{js}'][btn]['{side}']['{led}']['active']".format(
                            nb=btn, js=joy_side, led=led_name, side=led_side )
                            
                    generatedDict['pressed'] += "        dprint('Button_' + str(btn) + "
                    generatedDict['pressed'] += "' led {led}')\n".format(led=led_name)
                    
                    if btype == 'toggle':
                        generatedDict['pressed_event'] = "\n    if event.is_pressed:\n"
                        generatedDict['pressed'] += "        {button}['active'] = not {val}\n".format(
                                button=button_led, val=value)
                        generatedDict['pressed'] += "        to_update['{js}']['{dev}'] = True\n".format(js=joy_side, dev=device)
                        
                    elif btype == 'hold':
                        generatedDict['pressed_event'] = "\n    if event.is_pressed:\n"
                        generatedDict['pressed'] += "        {button}['active'] = True\n".format(
                                button=button_led, js=joy_side, led=led_name, side=led_side)
                        generatedDict['pressed'] += "        to_update['{js}']['{dev}'] = True\n".format(js=joy_side, dev=device)
                        
                        generatedDict['released_event'] = "\n    else:\n"
                        generatedDict['released'] += "        {button}['active'] = False\n".format(
                                button=button_led, js=joy_side, led=led_name, side=led_side)
                        generatedDict['released'] += "        to_update['{js}']['{dev}'] = True\n".format(js=joy_side, dev=device)
                        
                    elif btype == 'timed':
                        generatedDict['pressed_event'] = "\n    if event.is_pressed:\n"
                        generatedDict['pressed'] += "        {button}['active'] = True\n".format(
                                button=button_led, js=joy_side, led=led_name, side=led_side)
                        
                        # Add a timer to button
                        generatedDict['pressed'] += "        timed_leds.append(".format(side=led_side) + '{ '
                        generatedDict['pressed'] += "'side':'{side}', 'device':'{dev}', 'led':'{led}',".format(
                                dev=device, led=led_name, side=led_side)
                        generatedDict['pressed'] += "'button':'{nb}', 'button_side': '{s}', ".format(
                                nb=btn, s=joy_side)
                        generatedDict['pressed'] += "'timer': period * 2})\n"
                        
                        generatedDict['pressed'] += "        to_update['{js}']['{dev}'] = True\n".format(js=joy_side, dev=device)
                    
                
            generated += generatedDict['header'] + generatedDict['comment']
            generated += generatedDict['pressed_event'] + generatedDict['pressed']
            generated += generatedDict['released_event'] + generatedDict['released']
    
    dprint( generated + "\n" )
    


# Do this, then
# [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 
#generateButtonEvents()




@LJoy.button(1)
def handleButton( event, joy ):
    btn = 1 # hold button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led H1')
        BUTTONS['left'][btn]['left']['H1']['active'] = True
        to_update['left']['master'] = True
        dprint('Button_' + str(btn) + ' led H2')
        BUTTONS['left'][btn]['left']['H2']['active'] = True
        to_update['left']['master'] = True
        dprint('Button_' + str(btn) + ' led H3')
        BUTTONS['left'][btn]['left']['H3']['active'] = True
        to_update['left']['master'] = True
        dprint('Button_' + str(btn) + ' led H4')
        BUTTONS['left'][btn]['left']['H4']['active'] = True
        to_update['left']['master'] = True

    else:
        BUTTONS['left'][btn]['left']['H1']['active'] = False
        to_update['left']['master'] = True
        BUTTONS['left'][btn]['left']['H2']['active'] = False
        to_update['left']['master'] = True
        BUTTONS['left'][btn]['left']['H3']['active'] = False
        to_update['left']['master'] = True
        BUTTONS['left'][btn]['left']['H4']['active'] = False
        to_update['left']['master'] = True


@LJoy.button(33)
def handleButton( event, joy ):
    btn = 33 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B1')
        BUTTONS['left'][btn]['left']['B1']['active'] = not BUTTONS['left'][btn]['left']['B1']['active']
        to_update['left']['slave'] = True


@LJoy.button(34)
def handleButton( event, joy ):
    btn = 34 # timed button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B2')
        BUTTONS['left'][btn]['left']['B2']['active'] = True
        timed_leds.append({ 'side':'left', 'device':'slave', 'led':'B2','button':'34', 'button_side': 'left', 'timer': period * 2})
        to_update['left']['slave'] = True


@LJoy.button(72)
def handleButton( event, joy ):
    btn = 72 # timed button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led GearIndicator')
        BUTTONS['left'][btn]['left']['GearIndicator']['active'] = True
        timed_leds.append({ 'side':'left', 'device':'slave', 'led':'GearIndicator','button':'72', 'button_side': 'left', 'timer': period * 2})
        to_update['left']['slave'] = True


@LJoy.button(74)
def handleButton( event, joy ):
    btn = 74 # hold button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led GearDownLeft')
        BUTTONS['left'][btn]['left']['GearDownLeft']['active'] = True
        to_update['left']['slave'] = True
        dprint('Button_' + str(btn) + ' led GearDownNose')
        BUTTONS['left'][btn]['left']['GearDownNose']['active'] = True
        to_update['left']['slave'] = True
        dprint('Button_' + str(btn) + ' led GearDownRight')
        BUTTONS['left'][btn]['left']['GearDownRight']['active'] = True
        to_update['left']['slave'] = True

    else:
        BUTTONS['left'][btn]['left']['GearDownLeft']['active'] = False
        to_update['left']['slave'] = True
        BUTTONS['left'][btn]['left']['GearDownNose']['active'] = False
        to_update['left']['slave'] = True
        BUTTONS['left'][btn]['left']['GearDownRight']['active'] = False
        to_update['left']['slave'] = True


@LJoy.button(73)
def handleButton( event, joy ):
    btn = 73 # hold button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led GearUpNose')
        BUTTONS['left'][btn]['left']['GearUpNose']['active'] = True
        to_update['left']['slave'] = True
        dprint('Button_' + str(btn) + ' led GearUpLeft')
        BUTTONS['left'][btn]['left']['GearUpLeft']['active'] = True
        to_update['left']['slave'] = True
        dprint('Button_' + str(btn) + ' led GearUpRight')
        BUTTONS['left'][btn]['left']['GearUpRight']['active'] = True
        to_update['left']['slave'] = True

    else:
        BUTTONS['left'][btn]['left']['GearUpNose']['active'] = False
        to_update['left']['slave'] = True
        BUTTONS['left'][btn]['left']['GearUpLeft']['active'] = False
        to_update['left']['slave'] = True
        BUTTONS['left'][btn]['left']['GearUpRight']['active'] = False
        to_update['left']['slave'] = True


@LJoy.button(42)
def handleButton( event, joy ):
    btn = 42 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B10')
        BUTTONS['left'][btn]['left']['B10']['active'] = not BUTTONS['left'][btn]['left']['B10']['active']
        to_update['left']['slave'] = True


@LJoy.button(37)
def handleButton( event, joy ):
    btn = 37 # timed button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B5')
        BUTTONS['left'][btn]['left']['B5']['active'] = True
        timed_leds.append({ 'side':'left', 'device':'slave', 'led':'B5','button':'37', 'button_side': 'left', 'timer': period * 2})
        to_update['left']['slave'] = True


@LJoy.button(39)
def handleButton( event, joy ):
    btn = 39 # timed button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B7')
        BUTTONS['left'][btn]['left']['B7']['active'] = True
        timed_leds.append({ 'side':'left', 'device':'slave', 'led':'B7','button':'39', 'button_side': 'left', 'timer': period * 2})
        to_update['left']['slave'] = True


@LJoy.button(41)
def handleButton( event, joy ):
    btn = 41 # timed button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B9')
        BUTTONS['left'][btn]['left']['B9']['active'] = True
        timed_leds.append({ 'side':'left', 'device':'slave', 'led':'B9','button':'41', 'button_side': 'left', 'timer': period * 2})
        to_update['left']['slave'] = True


@RJoy.button(33)
def handleButton( event, joy ):
    btn = 33 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B1')
        BUTTONS['right'][btn]['right']['B1']['active'] = not BUTTONS['right'][btn]['right']['B1']['active']
        to_update['right']['slave'] = True


@RJoy.button(34)
def handleButton( event, joy ):
    btn = 34 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B2')
        BUTTONS['right'][btn]['right']['B2']['active'] = not BUTTONS['right'][btn]['right']['B2']['active']
        to_update['right']['slave'] = True
        dprint('Button_' + str(btn) + ' led B3')
        BUTTONS['right'][btn]['right']['B3']['active'] = not BUTTONS['right'][btn]['right']['B3']['active']
        to_update['right']['slave'] = True


@RJoy.button(39)
def handleButton( event, joy ):
    btn = 39 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B7')
        BUTTONS['right'][btn]['right']['B7']['active'] = not BUTTONS['right'][btn]['right']['B7']['active']
        to_update['right']['slave'] = True


@RJoy.button(42)
def handleButton( event, joy ):
    btn = 42 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B10')
        BUTTONS['right'][btn]['right']['B10']['active'] = not BUTTONS['right'][btn]['right']['B10']['active']
        to_update['right']['slave'] = True


@RJoy.button(43)
def handleButton( event, joy ):
    btn = 43 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B11')
        BUTTONS['right'][btn]['right']['B11']['active'] = not BUTTONS['right'][btn]['right']['B11']['active']
        to_update['right']['slave'] = True


@RJoy.button(44)
def handleButton( event, joy ):
    btn = 44 # toggle button

    if event.is_pressed:
        dprint('Button_' + str(btn) + ' led B12')
        BUTTONS['right'][btn]['right']['B12']['active'] = not BUTTONS['right'][btn]['right']['B12']['active']
        to_update['right']['slave'] = True

