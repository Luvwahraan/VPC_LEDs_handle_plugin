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

    dprint( 'Building empty for ' + device + ' ' + str(data) )
    
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


def generateButtonEvents():
    generated = ''
    
    for joy_side in ['left','right']:
        thisJoy = ''
        if joy_side == 'left':
            thisJoy = 'LJoy'
        elif joy_side == 'right':
            thisJoy = 'RJoy'
    
        for btn in BUTTONS[joy_side].keys():
            generatedHeader = """
@{j}.button({nb})
def handleButton( event, joy ):
""".format(j=thisJoy, nb=btn)

            generatedButton = ''
            generatedEvent = """    if event.is_pressed:
        dprint( 'Button ' + str({nb}) + ' pushed' )
    """.format(nb=btn)
            
            for led_side in BUTTONS[joy_side][btn].keys():
                for led_name in BUTTONS[joy_side][btn][led_side].keys():
                    device = BUTTONS[joy_side][btn][led_side][led_name]['device']
                    dprint('Button' + str(btn) + ' led ' + led_name )
                    
                    if BUTTONS[joy_side][btn][led_side][led_name]['type'] == 'hold':
                        generatedEvent = "    dprint( 'Button ' + str({nb}) + ' pushed' )\n".format(nb=btn)
                        spacer = ''
                    else:
                        spacer = '    '
                    
                    dprint('ok')
                    
                    # Replace colorname by value
                    color = colorMap[ BUTTONS[joy_side][btn][led_side][led_name]['color'] ]
                    
                    generatedButton += """
{sp}    if BUTTONS['{js}'][{nb}]['{side}']['{led}']['active']:
{sp}        dprint( 'Set LED {led} on {side} {dev} to off.' )
{sp}        BUTTONS['{js}'][{nb}]['{side}']['{led}']['active'] = False
{sp}    else:
{sp}        dprint( 'Set LED {led} on {side} {dev} to on.' )
{sp}        BUTTONS['{js}'][{nb}]['{side}']['{led}']['active'] = True
{sp}    
{sp}    to_update['{js}']['{dev}'] = True
""".format(nb=btn, js=joy_side, led=led_name, side=led_side, dev=device, sp=spacer)
    
            generated += generatedHeader + generatedEvent + generatedButton
    
    dprint(  generated + "\n\n"+'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} ')
    


@gremlin.input_devices.periodic(0.25)
def sendReportFeatures():
    #dprint('Periodic callback' + str(to_update) )
    
    for side in to_update.keys():
        ThisJoy = JDecorators[side]
        for device in to_update[side].keys():
            if to_update[side][device]:
                if device == 'slave':
                    slave_device = True
                else:
                    slave_device = False
                
                try:
                    #dprint('Try to build data for ' + device)
                    report_feature = buildReportFeature(side, slave=slave_device)
                    
                    dprint('Sending feature for ' + side + ' ' + device + ':' + str(report_feature) + ' on port ' + str( sock_clients[side].getPort() ) )
                    sock_clients[side].clientSend( bytes(report_feature) )
                    
                    # We don't need to do this until next update
                    to_update[side][device] = False
                except:
                    dprint( traceback.format_exc() )

LJoy = JDecorators['left']
RJoy = JDecorators['right']

# Do this, then
# [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 
#generateButtonEvents()



@LJoy.button(1)
def handleButton( event, joy ):
    dprint( 'Button ' + str(1) + ' pushed' )

    if BUTTONS['left'][1]['left']['H1']['active']:
        dprint( 'Set LED H1 on left master to off.' )
        BUTTONS['left'][1]['left']['H1']['active'] = False
    else:
        dprint( 'Set LED H1 on left master to on.' )
        BUTTONS['left'][1]['left']['H1']['active'] = True
    
    to_update['left']['master'] = True

    if BUTTONS['left'][1]['left']['H2']['active']:
        dprint( 'Set LED H2 on left master to off.' )
        BUTTONS['left'][1]['left']['H2']['active'] = False
    else:
        dprint( 'Set LED H2 on left master to on.' )
        BUTTONS['left'][1]['left']['H2']['active'] = True
    
    to_update['left']['master'] = True

    if BUTTONS['left'][1]['left']['H3']['active']:
        dprint( 'Set LED H3 on left master to off.' )
        BUTTONS['left'][1]['left']['H3']['active'] = False
    else:
        dprint( 'Set LED H3 on left master to on.' )
        BUTTONS['left'][1]['left']['H3']['active'] = True
    
    to_update['left']['master'] = True

    if BUTTONS['left'][1]['left']['H4']['active']:
        dprint( 'Set LED H4 on left master to off.' )
        BUTTONS['left'][1]['left']['H4']['active'] = False
    else:
        dprint( 'Set LED H4 on left master to on.' )
        BUTTONS['left'][1]['left']['H4']['active'] = True
    
    to_update['left']['master'] = True

@LJoy.button(33)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(33) + ' pushed' )
    
        if BUTTONS['left'][33]['left']['B1']['active']:
            dprint( 'Set LED B1 on left slave to off.' )
            BUTTONS['left'][33]['left']['B1']['active'] = False
        else:
            dprint( 'Set LED B1 on left slave to on.' )
            BUTTONS['left'][33]['left']['B1']['active'] = True
        
        to_update['left']['slave'] = True

@LJoy.button(34)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(34) + ' pushed' )
    
        if BUTTONS['left'][34]['left']['B2']['active']:
            dprint( 'Set LED B2 on left slave to off.' )
            BUTTONS['left'][34]['left']['B2']['active'] = False
        else:
            dprint( 'Set LED B2 on left slave to on.' )
            BUTTONS['left'][34]['left']['B2']['active'] = True
        
        to_update['left']['slave'] = True

@LJoy.button(72)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(72) + ' pushed' )
    
        if BUTTONS['left'][72]['left']['GearIndicator']['active']:
            dprint( 'Set LED GearIndicator on left slave to off.' )
            BUTTONS['left'][72]['left']['GearIndicator']['active'] = False
        else:
            dprint( 'Set LED GearIndicator on left slave to on.' )
            BUTTONS['left'][72]['left']['GearIndicator']['active'] = True
        
        to_update['left']['slave'] = True

@LJoy.button(74)
def handleButton( event, joy ):
    dprint( 'Button ' + str(74) + ' pushed' )

    if BUTTONS['left'][74]['left']['GearDownLeft']['active']:
        dprint( 'Set LED GearDownLeft on left slave to off.' )
        BUTTONS['left'][74]['left']['GearDownLeft']['active'] = False
    else:
        dprint( 'Set LED GearDownLeft on left slave to on.' )
        BUTTONS['left'][74]['left']['GearDownLeft']['active'] = True
    
    to_update['left']['slave'] = True

    if BUTTONS['left'][74]['left']['GearDownNose']['active']:
        dprint( 'Set LED GearDownNose on left slave to off.' )
        BUTTONS['left'][74]['left']['GearDownNose']['active'] = False
    else:
        dprint( 'Set LED GearDownNose on left slave to on.' )
        BUTTONS['left'][74]['left']['GearDownNose']['active'] = True
    
    to_update['left']['slave'] = True

    if BUTTONS['left'][74]['left']['GearDownRight']['active']:
        dprint( 'Set LED GearDownRight on left slave to off.' )
        BUTTONS['left'][74]['left']['GearDownRight']['active'] = False
    else:
        dprint( 'Set LED GearDownRight on left slave to on.' )
        BUTTONS['left'][74]['left']['GearDownRight']['active'] = True
    
    to_update['left']['slave'] = True

@LJoy.button(73)
def handleButton( event, joy ):
    dprint( 'Button ' + str(73) + ' pushed' )

    if BUTTONS['left'][73]['left']['GearUpNose']['active']:
        dprint( 'Set LED GearUpNose on left slave to off.' )
        BUTTONS['left'][73]['left']['GearUpNose']['active'] = False
    else:
        dprint( 'Set LED GearUpNose on left slave to on.' )
        BUTTONS['left'][73]['left']['GearUpNose']['active'] = True
    
    to_update['left']['slave'] = True

    if BUTTONS['left'][73]['left']['GearUpLeft']['active']:
        dprint( 'Set LED GearUpLeft on left slave to off.' )
        BUTTONS['left'][73]['left']['GearUpLeft']['active'] = False
    else:
        dprint( 'Set LED GearUpLeft on left slave to on.' )
        BUTTONS['left'][73]['left']['GearUpLeft']['active'] = True
    
    to_update['left']['slave'] = True

    if BUTTONS['left'][73]['left']['GearUpRight']['active']:
        dprint( 'Set LED GearUpRight on left slave to off.' )
        BUTTONS['left'][73]['left']['GearUpRight']['active'] = False
    else:
        dprint( 'Set LED GearUpRight on left slave to on.' )
        BUTTONS['left'][73]['left']['GearUpRight']['active'] = True
    
    to_update['left']['slave'] = True

@LJoy.button(42)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(42) + ' pushed' )
    
        if BUTTONS['left'][42]['left']['B10']['active']:
            dprint( 'Set LED B10 on left slave to off.' )
            BUTTONS['left'][42]['left']['B10']['active'] = False
        else:
            dprint( 'Set LED B10 on left slave to on.' )
            BUTTONS['left'][42]['left']['B10']['active'] = True
        
        to_update['left']['slave'] = True

@LJoy.button(37)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(37) + ' pushed' )
    
        if BUTTONS['left'][37]['left']['B5']['active']:
            dprint( 'Set LED B5 on left slave to off.' )
            BUTTONS['left'][37]['left']['B5']['active'] = False
        else:
            dprint( 'Set LED B5 on left slave to on.' )
            BUTTONS['left'][37]['left']['B5']['active'] = True
        
        to_update['left']['slave'] = True

@LJoy.button(39)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(39) + ' pushed' )
    
        if BUTTONS['left'][39]['left']['B7']['active']:
            dprint( 'Set LED B7 on left slave to off.' )
            BUTTONS['left'][39]['left']['B7']['active'] = False
        else:
            dprint( 'Set LED B7 on left slave to on.' )
            BUTTONS['left'][39]['left']['B7']['active'] = True
        
        to_update['left']['slave'] = True

@LJoy.button(41)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(41) + ' pushed' )
    
        if BUTTONS['left'][41]['left']['B9']['active']:
            dprint( 'Set LED B9 on left slave to off.' )
            BUTTONS['left'][41]['left']['B9']['active'] = False
        else:
            dprint( 'Set LED B9 on left slave to on.' )
            BUTTONS['left'][41]['left']['B9']['active'] = True
        
        to_update['left']['slave'] = True

@RJoy.button(33)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(33) + ' pushed' )
    
        if BUTTONS['right'][33]['right']['B1']['active']:
            dprint( 'Set LED B1 on right slave to off.' )
            BUTTONS['right'][33]['right']['B1']['active'] = False
        else:
            dprint( 'Set LED B1 on right slave to on.' )
            BUTTONS['right'][33]['right']['B1']['active'] = True
        
        to_update['right']['slave'] = True

@RJoy.button(34)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(34) + ' pushed' )
    
        if BUTTONS['right'][34]['left']['B3']['active']:
            dprint( 'Set LED B3 on left slave to off.' )
            BUTTONS['right'][34]['left']['B3']['active'] = False
        else:
            dprint( 'Set LED B3 on left slave to on.' )
            BUTTONS['right'][34]['left']['B3']['active'] = True
        
        to_update['right']['slave'] = True

        if BUTTONS['right'][34]['right']['B2']['active']:
            dprint( 'Set LED B2 on right slave to off.' )
            BUTTONS['right'][34]['right']['B2']['active'] = False
        else:
            dprint( 'Set LED B2 on right slave to on.' )
            BUTTONS['right'][34]['right']['B2']['active'] = True
        
        to_update['right']['slave'] = True

        if BUTTONS['right'][34]['right']['B3']['active']:
            dprint( 'Set LED B3 on right slave to off.' )
            BUTTONS['right'][34]['right']['B3']['active'] = False
        else:
            dprint( 'Set LED B3 on right slave to on.' )
            BUTTONS['right'][34]['right']['B3']['active'] = True
        
        to_update['right']['slave'] = True

@RJoy.button(39)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(39) + ' pushed' )
    
        if BUTTONS['right'][39]['right']['B7']['active']:
            dprint( 'Set LED B7 on right slave to off.' )
            BUTTONS['right'][39]['right']['B7']['active'] = False
        else:
            dprint( 'Set LED B7 on right slave to on.' )
            BUTTONS['right'][39]['right']['B7']['active'] = True
        
        to_update['right']['slave'] = True

@RJoy.button(42)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(42) + ' pushed' )
    
        if BUTTONS['right'][42]['right']['B10']['active']:
            dprint( 'Set LED B10 on right slave to off.' )
            BUTTONS['right'][42]['right']['B10']['active'] = False
        else:
            dprint( 'Set LED B10 on right slave to on.' )
            BUTTONS['right'][42]['right']['B10']['active'] = True
        
        to_update['right']['slave'] = True

@RJoy.button(43)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(43) + ' pushed' )
    
        if BUTTONS['right'][43]['right']['B11']['active']:
            dprint( 'Set LED B11 on right slave to off.' )
            BUTTONS['right'][43]['right']['B11']['active'] = False
        else:
            dprint( 'Set LED B11 on right slave to on.' )
            BUTTONS['right'][43]['right']['B11']['active'] = True
        
        to_update['right']['slave'] = True

@RJoy.button(44)
def handleButton( event, joy ):
    if event.is_pressed:
        dprint( 'Button ' + str(44) + ' pushed' )
    
        if BUTTONS['right'][44]['right']['B12']['active']:
            dprint( 'Set LED B12 on right slave to off.' )
            BUTTONS['right'][44]['right']['B12']['active'] = False
        else:
            dprint( 'Set LED B12 on right slave to on.' )
            BUTTONS['right'][44]['right']['B12']['active'] = True
        
        to_update['right']['slave'] = True