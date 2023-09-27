import sys
import logging

import gremlin
from gremlin.user_plugin import *
import logging
mode_global = ModeVariable("Global", "gl")

def dprint( string ):
    if 'gremlin' not in sys.modules:
        print( string )
    else:
        gremlin.util.log( string )

try:
    from plugins_stuff import *
    from data import LedNames, ColorMap, LED, LedBank
except:
    sys.path.append(sys.path[0]+'\\plugins\\VPC_LEDs_handle_plugin.')
    from plugins_stuff import *
    from data import LedNames, ColorMap, LED, LedBank
    

period = 750 # ms
# Periodic LEDs update is period/3 (250ms)
# Timers default time is period * 2, and decrease each period



LEFT_GUID = '{FE8A3740-140F-11EE-8003-444553540000}'
RIGHT_GUID = '{2E6F6CA0-141F-11EE-8005-444553540000}'

Joysticks = {
    LEFT_GUID: {
        'name': 'LJoy',
        'decorator': gremlin.input_devices.JoystickDecorator(
                "LEFT VPC AlphaP CP2",
                LEFT_GUID,
                mode_global.value ),
        'banks': {
            'master': LedNames.alpha_prime,
            'slave': LedNames.panel2
        },
    },
    RIGHT_GUID: {
        'name': 'RJoy',
        'decorator': gremlin.input_devices.JoystickDecorator(
                "RIGHT VPC AlphaP CP1",
                RIGHT_GUID,
                mode_global.value ),
        'banks': {
            'master': LedNames.alpha_prime,
            'slave': LedNames.panel1
        },
    },
}
    
LJoy = Joysticks[LEFT_GUID]['decorator']
RJoy = Joysticks[RIGHT_GUID]['decorator']


# Periodic callback will update device setted to True
to_update = {
    RIGHT_GUID: {'master': True, 'slave': True},
    LEFT_GUID: {'master': True, 'slave': True},
    }

# Timed LED list
timed_leds = []

BUTTONS = {
    RIGHT_GUID: { # Physical joystick guid
        33: {                                   # Physical joystick button number
            'description': 'Do thing',          # (optionnal)
            'type':'toggle',                    # toggle, hold, timed
            RIGHT_GUID: LedBank( [
                    LED( name='B1',             # Button name on panel or grip; see list above
                        number=LedNames.getLedNumber('B1',Joysticks[RIGHT_GUID]['banks']['slave']),
                        device=RIGHT_GUID,      # LED's joystick guid
                        colorName='white-dim'   # See ColorMap
                    ),
                ],
                slave=True ),
        },
        34: {
            'type':'toggle',
            RIGHT_GUID: LedBank( [
                    LED( name='B3',
                        number=LedNames.getLedNumber('B3',Joysticks[RIGHT_GUID]['banks']['slave']),
                        device=RIGHT_GUID,
                        colorName='white-dim'
                    ),
                ],
                slave=True ),
        },
        39: {
            'description': 'Quantum MODE',
            'type':'toggle',
            RIGHT_GUID: LedBank( [
                    LED( name='B7',
                        number=LedNames.getLedNumber('B7',Joysticks[RIGHT_GUID]['banks']['slave']),
                        device=RIGHT_GUID,
                        colorName='yellow-dim'
                    ),
                ],
                slave=True ),
        },
        42: {
            'description': 'Weapons power toggle',
            'type':'toggle',
            RIGHT_GUID: LedBank( [
                    LED( name='B10',
                        number=LedNames.getLedNumber('B10',Joysticks[RIGHT_GUID]['banks']['slave']),
                        device=RIGHT_GUID,
                        colorName='red-dim'
                    ),
                ],
                slave=True ),
        },
        43: {
            'description': 'Engine power toggle',
            'type':'toggle',
            RIGHT_GUID: LedBank( [
                    LED( name='B11',
                        number=LedNames.getLedNumber('B11',Joysticks[RIGHT_GUID]['banks']['slave']),
                        device=RIGHT_GUID,
                        colorName='cyan-dim'
                    ),
                ],
                slave=True ),
        },
        44: {
            'description': 'Shields power toggle',
            'type':'toggle',
            RIGHT_GUID: LedBank( [
                    LED( name='B12',
                        number=LedNames.getLedNumber('B12',Joysticks[RIGHT_GUID]['banks']['slave']),
                        device=RIGHT_GUID,
                        colorName='green-dim'
                    ),
                ],
                slave=True ),
        },
    },
    LEFT_GUID: {
        1: {
            'description': 'Fire 1 active',
            'type':'hold',
            LEFT_GUID: LedBank( [
                    LED( name='H1',
                        number=LedNames.getLedNumber('H1',Joysticks[LEFT_GUID]['banks']['master']),
                        device=LEFT_GUID,
                        slave=False,
                        colorName='red'
                    ),
                ],
                slave=False ),
            LEFT_GUID: LedBank( [
                    LED( name='H3',
                        number=LedNames.getLedNumber('H3',Joysticks[LEFT_GUID]['banks']['master']),
                        device=LEFT_GUID,
                        slave=False,
                        colorName='red'
                    ),
                ],
                slave=False ),
        },
        33: {
            'description': 'Lights toggle',
            'type':'toggle',
            LEFT_GUID: LedBank( [
                    LED( name='B1',
                        number=LedNames.getLedNumber('B1',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='blue-dim'
                    ),
                ],
                slave=True ),
        },
        34: {
            'description': 'Call ATC',
            'type':'timed',
            LEFT_GUID: LedBank( [
                    LED( name='B2',
                        number=LedNames.getLedNumber('B2',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='blue-dim'
                    ),
                ],
                slave=True ),
        },
        72: {
            'description': 'Gears up / retract',
            'type':'timed',
            LEFT_GUID: LedBank( [
                    LED( name='GearIndicator',
                        number=LedNames.getLedNumber('GearIndicator',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='red-dim'
                    ),
                ],
                slave=True ),
        },
        74: {
            'description': 'Gears down',
            'type':'hold',
            LEFT_GUID: LedBank( [
                    LED( name='GearDownLeft',
                        number=LedNames.getLedNumber('GearDownLeft',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='green-dim'
                    ),
                    LED( name='GearDownNose',
                        number=LedNames.getLedNumber('GearDownNose',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='green-dim'
                    ),
                    LED( name='GearDownRight',
                        number=LedNames.getLedNumber('GearDownRight',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='green-dim'
                    ),
                ],
                slave=True ),
        },
        73: {
            'description': 'Expand',
            'type':'hold',
            LEFT_GUID: LedBank( [
                    LED( name='GearUpLeft',
                        number=LedNames.getLedNumber('GearUpLeft',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='green-dim'
                    ),
                    LED( name='GearUpNose',
                        number=LedNames.getLedNumber('GearUpNose',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='green-dim'
                    ),
                    LED( name='GearUpRight',
                        number=LedNames.getLedNumber('GearUpRight',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='green-dim'
                    ),
                ],
                slave=True ),
        },
        42: {
            'type':'toggle',
            LEFT_GUID: LedBank( [
                    LED( name='B10',
                        number=LedNames.getLedNumber('B10',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='red'
                    ),
                ],
                slave=True ),
        },
        36: {
            'description':'Seat out',
            'type':'timed',
            LEFT_GUID: LedBank( [
                    LED( name='B4',
                        number=LedNames.getLedNumber('B4',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='yellow-dim'
                    ),
                ],
                slave=True ),
        },
        37: {
            'description': 'Turret 1',
            'type':'timed',
            LEFT_GUID: LedBank( [
                    LED( name='B5',
                        number=LedNames.getLedNumber('B5',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='yellow-dim'
                    ),
                ],
                slave=True ),
        },
        39: {
            'description': 'Turret 2',
            'type':'timed',
            LEFT_GUID: LedBank( [
                    LED( name='B7',
                        number=LedNames.getLedNumber('B7',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='yellow-dim'
                    ),
                ],
                slave=True ),
        },
        41: {
            'description': 'Turret 3',
            'type':'timed',
            LEFT_GUID: LedBank( [
                    LED( name='B9',
                        number=LedNames.getLedNumber('B9',Joysticks[LEFT_GUID]['banks']['slave']),
                        device=LEFT_GUID,
                        colorName='yellow-dim'
                    ),
                ],
                slave=True ),
            RIGHT_GUID: LedBank( [
                    LED( name='B8',
                        number=LedNames.getLedNumber('B8',Joysticks[RIGHT_GUID]['banks']['slave']),
                        device=RIGHT_GUID,
                        colorName='salmon'
                    ),
                ],
                slave=True ),
        },
    },
}


def buildReportFeature(led_js_guid, slave=False ):
    data = [0x02]
    
    if slave:
        data += [0x67, 0x00, 0x00, 0x00]
        data += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    else:
        data += [0x68, 0x00, 0x00, 0x00]
        data += [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
    
    data.append(0xf0)

    #dprint( 'Building empty for ' + led_js_guid )
    
    # Searching for led_js_guid's LED in all joystick's buttons...
    for btn_js_guid in BUTTONS.keys():
        #dprint( '  list joystick by guid ' + btn_js_guid )
        
        for btn in BUTTONS[btn_js_guid].keys():
            #dprint( '    button_' + str( btn ) )
            
            try:
                if led_js_guid in BUTTONS[btn_js_guid][btn]:
                    #dprint( "      led_js_guid "+str(led_js_guid) )
                    
                    for led in BUTTONS[btn_js_guid][btn][led_js_guid].bank.values():
                        #dprint( "        led "+led.name )
                        #dprint( "        LedBank "+str(BUTTONS[btn_js_guid][btn][led_js_guid].__dict__.keys()) )
                        
                        # ... but only for master or slave
                        if BUTTONS[btn_js_guid][btn][led_js_guid].slave == slave:
                            
                            if led.active:
                                color = led.color
                                #dprint( 'Coloring ' + str(color) )
                            else:
                                #dprint( 'Turning off' )
                                color = ColorMap.getValue('off')
                            
                            # Searching LED number to change
                            if slave:
                                ms_type = 'slave'
                            else:
                                ms_type = 'master'
                            joystick = Joysticks[led_js_guid]['banks'][ms_type]
                            
                            # Add 5 cause LEDs begins at byte 5 in feature report
                            led_nb = LedNames.getLedNumber(led.name, joystick) + 5
                            
                            #dprint( '      updating led ' + str(led_nb) )
                            data[led_nb] = color
            except:
                #dprint( traceback.format_exc() )
                pass
    
    return data

sock_clients = {
    LEFT_GUID: ConnectHandle( client=True, port=14517 ),
    RIGHT_GUID: ConnectHandle( client=True, port=14518 )
    }



@gremlin.input_devices.periodic(period / 1000)
def checkTimed():
    """
    Check times_leds list to handle timers.
    """
    
    if len( timed_leds ) > 0:
        dprint('timed callback timer ' + str(timed_leds) )
        pass
    
    to_delete = []
    try:
        for led_nb in range( len(timed_leds) ):
            btn_js_guid = timed_leds[led_nb]['button_js_guid']
            button = int(timed_leds[led_nb]['button'])
            led_js_guid = timed_leds[led_nb]['led_js_guid']
            led_name = timed_leds[led_nb]['led']
            led_dev = timed_leds[led_nb]['device']
            
            if timed_leds[led_nb]['timer'] > 0:
                timed_leds[led_nb]['timer'] -= period
            else:
                dprint("Checking BUTTONS['{s}'][{b}]['{sl}']['{l}']".format(b=button,s=btn_js_guid,l=led_name,sl=led_js_guid) )
                BUTTONS[btn_js_guid][button][led_js_guid].bank[led_name].active = False
                to_update[led_js_guid][led_dev] = True
                to_delete.append( led_nb )
    except:
        dprint( traceback.format_exc() )
        pass
        
    if len( to_delete ) > 0:
        to_delete.sort(reverse=True)
        for led_nb in to_delete:
            del( timed_leds[led_nb] )
    

@gremlin.input_devices.periodic(period / 3000)
def checkUpdates():
    #dprint('Periodic callback' + str(to_update) )
    
    for js_guid_update in to_update.keys():
        ThisJoy = Joysticks[js_guid_update]['decorator']
        
        for device_type in to_update[js_guid_update].keys():
        
            # Update buttons who have to
            if to_update[js_guid_update][device_type]:
                #dprint('Periodic callback update: ' + js_guid_update + ' ' + device_type )
                
                if device_type == 'slave':
                    slave_device = True
                else:
                    slave_device = False
                
                try:
                    #dprint('Try to build data for ' + device_type)
                    report_feature = buildReportFeature(js_guid_update, slave=slave_device)
                    
                    dprint('Sending feature for ' + js_guid_update + ' ' + device_type + ':' + str(report_feature) + ' on port ' + str( sock_clients[js_guid_update].getPort() ) )
                    sock_clients[js_guid_update].clientSend( bytes(report_feature) )
                    
                    # We don't need to update until next change
                    to_update[js_guid_update][device_type] = False
                except:
                    dprint( traceback.format_exc() )
                    pass
            
        
    




def generateButtonEvents():
    generated = ''
    generatedDict = {
        'pressed_event': '',
        'pressed': '',
        'released_event': '',
        'released': '',
    }
    
    for btn_js_guid in Joysticks.keys():
        thisJoy = Joysticks[btn_js_guid]['name']
        generatedDict['guid'] = "    btn_js_guid = '{g}'\n".format(g=btn_js_guid)
    
        for btn in BUTTONS[btn_js_guid].keys():
            generatedDict['header'] = "@{j}.button({nb})\n".format(j=thisJoy, nb=btn)
            generatedDict['header'] += "def handleButton( event, joy ):\n    btn = {nb}".format(nb=btn)
            
            if 'description' in BUTTONS[btn_js_guid][btn]:
                generated += "\n\n# "+ BUTTONS[btn_js_guid][btn]['description'] + "\n"
            else:
                generated += "\n\n"
            
            generated += generatedDict['header']
            
            btype = BUTTONS[btn_js_guid][btn]['type']
            generated += " # {t} button\n\n".format(t=btype)
            
            events_str = {
                    'pressed_event': {
                        'events':[],
                        'updates':{},
                        'vars':[],
                    },
                    'released_event': {
                        'events':[],
                        'updates':{},
                        'vars':[],
                    },
            }
            
            for led_js_guid in BUTTONS[btn_js_guid][btn].keys():
            
                #dprint( "Generating for {bg}:{b} -> {lg} ".format(
                #        bg=btn_js_guid,b=btn,lg=led_js_guid) )
                #dprint( "Generating for {b}".format(b=btn) )
                
                if isinstance( BUTTONS[btn_js_guid][btn][led_js_guid], LedBank):
                    generatedDict['pressed_event'] = ''
                    generatedDict['pressed'] = ''
                    generatedDict['released_event'] = ''
                    generatedDict['released'] = ''
                    
                    events_str['pressed_event']['vars'].append(f"    guid_btn = '{btn_js_guid}'\n")
                    
                    for led in BUTTONS[btn_js_guid][btn][led_js_guid].bank.values():
                        #dprint("\t Lets go doing "+led.name)
                        
                        events_str['pressed_event']['vars'].append(f"    guid_led_{led.name} = '{led.device}'\n")
                        

                        
                        # LedBank is for master or slave device?
                        led_dev = 'master'
                        if BUTTONS[btn_js_guid][btn][led_js_guid].slave:
                            led_dev = 'slave'
                        
                        # Shorter to write, more readable. ;)
                        button = f"BUTTONS[guid_btn][btn][guid_led_{led.name}].bank['{led.name}']"
                        events_str['pressed_event']['vars'].append( f"    btn_{led.name} = {button}\n" )
                        
                        if btype == 'toggle':
                            string = f"        btn_{led.name}.active = not btn_{led.name}.active\n\n"
                            events_str['pressed_event']['events'].append(string)
                            events_str['pressed_event']['updates'][led_js_guid] = led_dev
                            
                            #dprint( "\t\ttoggle led is "+led_dev )
                            
                        elif btype == 'hold':
                            string = f"        btn_{led.name}.active = True\n"
                            events_str['pressed_event']['events'].append(string)
                            events_str['pressed_event']['updates'][led_js_guid] = led_dev
                            
                            string = f"        btn_{led.name}.active = False\n\n"
                            events_str['released_event']['events'].append(string)
                            events_str['released_event']['updates'][led_js_guid] = led_dev
                            
                            #dprint( "\t\thold led" )
                            
                        elif btype == 'timed':
                            string = f"        btn_{led.name}.active = True\n"
                            
                            # Add a timer to button
                            string += "        timed_leds.append({ "
                            string += "'led_js_guid':guid_led_{l}, 'device':'{d}', 'led':'{l}',".format(
                                    d=led_dev, l=led.name)
                            string += f"'button':'{btn}',\n                'button_js_guid': guid_btn, "
                            string += "'timer': period * 2 })\n\n"
                            
                            events_str['pressed_event']['events'].append(string)
                            events_str['pressed_event']['updates'][led_js_guid] = led_dev
                            
                            #dprint( "\t\ttimed led" )
                
            #generated += generatedDict['pressed_event'] + generatedDict['pressed']
            #generated += generatedDict['released_event'] + generatedDict['released']
            
            for e in events_str.keys():
                #dprint( e )
                
                # Don't do anything if there is no event to add.
                if len( events_str[e]['events'] ) > 0:
                    
                    # First add all leds vars
                    for s in events_str[e]['vars']:
                        #dprint( s )
                        generated += s
                        
                    # Next event condition
                    if e == 'pressed_event':
                        generated += "\n    if event.is_pressed:\n"
                    elif e == 'released_event':
                        generated += "\n    else:\n"
                    
                    
                    # Then add all buttons
                    for s in events_str[e]['events']:
                        #dprint( s )
                        generated += s
                    
                    # And all led updates for this event
                    for k,v in events_str[e]['updates'].items():
                        #dprint(f"in loop: {k}:{v}")
                        s = "        to_update['{g}']['{d}'] = True\n".format(
                                        g=k,d=v)
                        #dprint( s )
                        generated += s
    
    dprint( generated + "\n" )
    


# Do this, then
# [0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} 
generateButtonEvents()


