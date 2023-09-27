
class ColorMap:
    colors = {
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
      'deep_salmon': 0b10000110,
      'red-orange': 0b10000111,
      'red-pink': 0b10010011,
      'pink': 0b10100111,
      'purple': 0b10110010,
      'indigo': 0b10100001,
      'light-blue': 0b10111010,
      'lime-green': 0b10001110
    }
    
    @classmethod
    def getValue( self, cname ):
        return self.colors[cname]
    
    @classmethod
    def getName( self, value ):
        if value > 255:
            raise Exception("Leds colors are 8bits (<=255)")
        
        for led_name, led_value in self.colors.items():
            if value == led_value:
                return led_name
        
        # No color found in dict.
        return ''
    
    

class LED():
    
    def setColor(self, color):
    
        # Can be set with color value instead of name.
        if isinstance(color, int):
            if color > 255 or color < 128:
                raise Exception("LED colors are 128+color, on 8bits.")
                
            # No value if unkown color
            self.colorName = ColorMap.getName(color)
            
            self.color = color
        else:
            # Should throw an error if doesn't exist
            self.color = ColorMap.getValue( color )
            self.colorName = color
        
    
    
    def __init__(self, name, number, device,
            slave=True, colorName='off', active=False):
        """
            name
                see led_names list
                
            colorName
                see ColorMap
            
            device
                what device the led is on: (JG guid)
            
            slave
                master or slave (boolean)
            
            number
                led position
            
            active (optional)
                True when LED on, else False
        """
        
        self.name = name
        self.device = device
        self.number = number
        self.slave = slave
        self.master = not slave
        self.colorName = colorName
        self.active = active
        
        
        self.color = 0
        self.setColor(colorName)
        
    

class LedBank:
    """
    Create a dict of LED objects.
    
    bank = { 'B2': LED(), 'B4':LED() }
    """
    
    def __init__(self, l_list, slave=True):
        self.slave = slave
        self.master = not slave
        self.bank = {}
        nb = 0
        
        for led in l_list:
            if isinstance( led, str):
                self.bank[led] = LED(led, nb, '', slave)
            elif isinstance( led, LED):
                self.bank[led.name] = led
            nb += 1
        
    def getNames(self):
        return self.bank.keys()
    
    # Returns all color values (uint8)
    def getValues(self):
        values = []
        for led in self.bank.values():
            values.append(led.color)
        
        return values
    
    # Returns all color values, but 'off' for inactives ones
    def getActiveValues(self):
        values = []
        for led in self.bank.values():
            if self.bank.active:
                values.append(led.color)
        else:
            values.append( ColorMap.getValue('off') )
        
        return values
    
        
    def setAllLeds(self, colorName='off'):
        for led in self.bank.keys():
            self.bank[led].setColor()
        
    


class LedNames:
    alpha_prime = LedBank( l_list=['S1', 'S2', 'S3', 'S4', 'S5', 'H1',
            'H2', 'H3', 'H4'], slave=False )
    panel1 = LedBank( l_list=['B10', 'B11', 'B12', 'B7', 'B8', 'B9', 'B6', 'B4',
            'B2', 'B5', 'B3', 'B1'], slave=True )
    panel2 = LedBank( l_list=['B2', 'B1', 'B4', 'B3',
            'GearUpNose', 'GearIndicator', 'GearUpLeft',
            'GearDownLeft', 'GearDownNose', 'GearDownRight', 'GearUpRight',
            'B10', 'B8', 'B6', 'B9', 'B7', 'B5'], slave=True )
            
    def getBank(bank_type='empty'):
        if bank_type == 'alpha_prime':
            return alpha_prime
        elif bank_type == 'panel1':
            return panel1
        elif bank_type == 'panel2':
            return panel2
        elif bank_type == 'empty':
            no_led = []
            for i in range(0, 31):
                no_led.append( i )
            return LedBank(no_led)
        
    
    def getLedNumber(led_name, led_device):
        return led_device.bank[led_name].number
        pass
    
    def getLedNames(led_device):
        return list( led_device.bank.keys() )
        pass