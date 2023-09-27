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
                    LED( name='H3',
                        number=LedNames.getLedNumber('H3',Joysticks[LEFT_GUID]['banks']['master']),
                        device=LEFT_GUID,
                        slave=False,
                        colorName='red'
                    ),
                ],
                slave=False ),
            RIGHT_GUID: LedBank( [
                    LED( name='H1',
                        number=LedNames.getLedNumber('H1',Joysticks[RIGHT_GUID]['banks']['master']),
                        device=RIGHT_GUID,
                        slave=False,
                        colorName='blue'
                    ),
                    LED( name='H3',
                        number=LedNames.getLedNumber('H3',Joysticks[RIGHT_GUID]['banks']['master']),
                        device=RIGHT_GUID,
                        slave=False,
                        colorName='blue'
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
                dprint("Checking BUTTONS['{s}'][{b}]['{sl}']['{l}']".format(
                        b=button,s=btn_js_guid,l=led_name,sl=led_js_guid) )
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
            
            
            d_nb = 0
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
                        
                        # if there is more one device with led, leds vars have to be unique
                        led_id = led.name + "_" + str(d_nb)
                        
                        events_str['pressed_event']['vars'].append(f"    guid_led_{led_id} = '{led.device}'\n")
                        
                        
                        # LedBank is for master or slave device?
                        led_dev = 'master'
                        if BUTTONS[btn_js_guid][btn][led_js_guid].slave:
                            led_dev = 'slave'
                        
                        # Shorter to write, more readable. ;)
                        button = f"BUTTONS[guid_btn][btn][guid_led_{led_id}].bank['{led.name}']"
                        events_str['pressed_event']['vars'].append( f"    btn_{led_id} = {button}\n" )
                        
                        if btype == 'toggle':
                            string = f"        btn_{led_id}.active = not btn_{led_id}.active\n\n"
                            events_str['pressed_event']['events'].append(string)
                            events_str['pressed_event']['updates'][led_js_guid] = led_dev
                            
                            #dprint( "\t\ttoggle led is "+led_dev )
                            
                        elif btype == 'hold':
                            string = f"        btn_{led_id}.active = True\n"
                            events_str['pressed_event']['events'].append(string)
                            events_str['pressed_event']['updates'][led_js_guid] = led_dev
                            
                            string = f"        btn_{led_id}.active = False\n"
                            events_str['released_event']['events'].append(string)
                            events_str['released_event']['updates'][led_js_guid] = led_dev
                            
                            #dprint( "\t\thold led" )
                            
                        elif btype == 'timed':
                            string = f"        btn_{led_id}.active = True\n"
                            
                            # Add a timer to button
                            string += "        timed_leds.append({ "
                            string += f"'led_js_guid':guid_led_{led_id}, 'device':'{led_dev}',"
                            string += f"'led':'{led.name}',"
                            string += f"'button':'{btn}',\n                'button_js_guid': guid_btn, "
                            string += "'timer': period * 2 })\n\n"
                            
                            events_str['pressed_event']['events'].append(string)
                            events_str['pressed_event']['updates'][led_js_guid] = led_dev
                            
                            #dprint( "\t\ttimed led" )
                        
                        d_nb += 1
                
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
#generateButtonEvents()


# Fire 1 active
@LJoy.button(1)
def handleButton( event, joy ):
    btn = 1 # hold button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_H1_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_H1_0 = BUTTONS[guid_btn][btn][guid_led_H1_0].bank['H1']
    guid_led_H3_1 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_H3_1 = BUTTONS[guid_btn][btn][guid_led_H3_1].bank['H3']
    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_H1_2 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_H1_2 = BUTTONS[guid_btn][btn][guid_led_H1_2].bank['H1']
    guid_led_H3_3 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_H3_3 = BUTTONS[guid_btn][btn][guid_led_H3_3].bank['H3']

    if event.is_pressed:
        btn_H1_0.active = True
        btn_H3_1.active = True
        btn_H1_2.active = True
        btn_H3_3.active = True
        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['master'] = True
        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['master'] = True

    else:
        btn_H1_0.active = False
        btn_H3_1.active = False
        btn_H1_2.active = False
        btn_H3_3.active = False
        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['master'] = True
        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['master'] = True


# Lights toggle
@LJoy.button(33)
def handleButton( event, joy ):
    btn = 33 # toggle button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B1_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_B1_0 = BUTTONS[guid_btn][btn][guid_led_B1_0].bank['B1']

    if event.is_pressed:
        btn_B1_0.active = not btn_B1_0.active

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Call ATC
@LJoy.button(34)
def handleButton( event, joy ):
    btn = 34 # timed button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B2_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_B2_0 = BUTTONS[guid_btn][btn][guid_led_B2_0].bank['B2']

    if event.is_pressed:
        btn_B2_0.active = True
        timed_leds.append({ 'led_js_guid':guid_led_B2_0, 'device':'slave','led':'B2','button':'34',
                'button_js_guid': guid_btn, 'timer': period * 2 })

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Gears up / retract
@LJoy.button(72)
def handleButton( event, joy ):
    btn = 72 # timed button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_GearIndicator_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_GearIndicator_0 = BUTTONS[guid_btn][btn][guid_led_GearIndicator_0].bank['GearIndicator']

    if event.is_pressed:
        btn_GearIndicator_0.active = True
        timed_leds.append({ 'led_js_guid':guid_led_GearIndicator_0, 'device':'slave','led':'GearIndicator','button':'72',
                'button_js_guid': guid_btn, 'timer': period * 2 })

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Gears down
@LJoy.button(74)
def handleButton( event, joy ):
    btn = 74 # hold button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_GearDownLeft_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_GearDownLeft_0 = BUTTONS[guid_btn][btn][guid_led_GearDownLeft_0].bank['GearDownLeft']
    guid_led_GearDownNose_1 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_GearDownNose_1 = BUTTONS[guid_btn][btn][guid_led_GearDownNose_1].bank['GearDownNose']
    guid_led_GearDownRight_2 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_GearDownRight_2 = BUTTONS[guid_btn][btn][guid_led_GearDownRight_2].bank['GearDownRight']

    if event.is_pressed:
        btn_GearDownLeft_0.active = True
        btn_GearDownNose_1.active = True
        btn_GearDownRight_2.active = True
        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True

    else:
        btn_GearDownLeft_0.active = False
        btn_GearDownNose_1.active = False
        btn_GearDownRight_2.active = False
        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Expand
@LJoy.button(73)
def handleButton( event, joy ):
    btn = 73 # hold button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_GearUpLeft_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_GearUpLeft_0 = BUTTONS[guid_btn][btn][guid_led_GearUpLeft_0].bank['GearUpLeft']
    guid_led_GearUpNose_1 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_GearUpNose_1 = BUTTONS[guid_btn][btn][guid_led_GearUpNose_1].bank['GearUpNose']
    guid_led_GearUpRight_2 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_GearUpRight_2 = BUTTONS[guid_btn][btn][guid_led_GearUpRight_2].bank['GearUpRight']

    if event.is_pressed:
        btn_GearUpLeft_0.active = True
        btn_GearUpNose_1.active = True
        btn_GearUpRight_2.active = True
        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True

    else:
        btn_GearUpLeft_0.active = False
        btn_GearUpNose_1.active = False
        btn_GearUpRight_2.active = False
        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


@LJoy.button(42)
def handleButton( event, joy ):
    btn = 42 # toggle button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B10_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_B10_0 = BUTTONS[guid_btn][btn][guid_led_B10_0].bank['B10']

    if event.is_pressed:
        btn_B10_0.active = not btn_B10_0.active

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Seat out
@LJoy.button(36)
def handleButton( event, joy ):
    btn = 36 # timed button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B4_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_B4_0 = BUTTONS[guid_btn][btn][guid_led_B4_0].bank['B4']

    if event.is_pressed:
        btn_B4_0.active = True
        timed_leds.append({ 'led_js_guid':guid_led_B4_0, 'device':'slave','led':'B4','button':'36',
                'button_js_guid': guid_btn, 'timer': period * 2 })

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Turret 1
@LJoy.button(37)
def handleButton( event, joy ):
    btn = 37 # timed button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B5_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_B5_0 = BUTTONS[guid_btn][btn][guid_led_B5_0].bank['B5']

    if event.is_pressed:
        btn_B5_0.active = True
        timed_leds.append({ 'led_js_guid':guid_led_B5_0, 'device':'slave','led':'B5','button':'37',
                'button_js_guid': guid_btn, 'timer': period * 2 })

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Turret 2
@LJoy.button(39)
def handleButton( event, joy ):
    btn = 39 # timed button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B7_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_B7_0 = BUTTONS[guid_btn][btn][guid_led_B7_0].bank['B7']

    if event.is_pressed:
        btn_B7_0.active = True
        timed_leds.append({ 'led_js_guid':guid_led_B7_0, 'device':'slave','led':'B7','button':'39',
                'button_js_guid': guid_btn, 'timer': period * 2 })

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True


# Turret 3
@LJoy.button(41)
def handleButton( event, joy ):
    btn = 41 # timed button

    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B9_0 = '{FE8A3740-140F-11EE-8003-444553540000}'
    btn_B9_0 = BUTTONS[guid_btn][btn][guid_led_B9_0].bank['B9']
    guid_btn = '{FE8A3740-140F-11EE-8003-444553540000}'
    guid_led_B8_1 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_B8_1 = BUTTONS[guid_btn][btn][guid_led_B8_1].bank['B8']

    if event.is_pressed:
        btn_B9_0.active = True
        timed_leds.append({ 'led_js_guid':guid_led_B9_0, 'device':'slave','led':'B9','button':'41',
                'button_js_guid': guid_btn, 'timer': period * 2 })

        btn_B8_1.active = True
        timed_leds.append({ 'led_js_guid':guid_led_B8_1, 'device':'slave','led':'B8','button':'41',
                'button_js_guid': guid_btn, 'timer': period * 2 })

        to_update['{FE8A3740-140F-11EE-8003-444553540000}']['slave'] = True
        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['slave'] = True


# Do thing
@RJoy.button(33)
def handleButton( event, joy ):
    btn = 33 # toggle button

    guid_btn = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    guid_led_B1_0 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_B1_0 = BUTTONS[guid_btn][btn][guid_led_B1_0].bank['B1']

    if event.is_pressed:
        btn_B1_0.active = not btn_B1_0.active

        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['slave'] = True


@RJoy.button(34)
def handleButton( event, joy ):
    btn = 34 # toggle button

    guid_btn = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    guid_led_B3_0 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_B3_0 = BUTTONS[guid_btn][btn][guid_led_B3_0].bank['B3']

    if event.is_pressed:
        btn_B3_0.active = not btn_B3_0.active

        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['slave'] = True


# Quantum MODE
@RJoy.button(39)
def handleButton( event, joy ):
    btn = 39 # toggle button

    guid_btn = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    guid_led_B7_0 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_B7_0 = BUTTONS[guid_btn][btn][guid_led_B7_0].bank['B7']

    if event.is_pressed:
        btn_B7_0.active = not btn_B7_0.active

        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['slave'] = True


# Weapons power toggle
@RJoy.button(42)
def handleButton( event, joy ):
    btn = 42 # toggle button

    guid_btn = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    guid_led_B10_0 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_B10_0 = BUTTONS[guid_btn][btn][guid_led_B10_0].bank['B10']

    if event.is_pressed:
        btn_B10_0.active = not btn_B10_0.active

        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['slave'] = True


# Engine power toggle
@RJoy.button(43)
def handleButton( event, joy ):
    btn = 43 # toggle button

    guid_btn = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    guid_led_B11_0 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_B11_0 = BUTTONS[guid_btn][btn][guid_led_B11_0].bank['B11']

    if event.is_pressed:
        btn_B11_0.active = not btn_B11_0.active

        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['slave'] = True


# Shields power toggle
@RJoy.button(44)
def handleButton( event, joy ):
    btn = 44 # toggle button

    guid_btn = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    guid_led_B12_0 = '{2E6F6CA0-141F-11EE-8005-444553540000}'
    btn_B12_0 = BUTTONS[guid_btn][btn][guid_led_B12_0].bank['B12']

    if event.is_pressed:
        btn_B12_0.active = not btn_B12_0.active

        to_update['{2E6F6CA0-141F-11EE-8005-444553540000}']['slave'] = True



