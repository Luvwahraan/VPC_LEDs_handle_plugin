
class ColorMap:
    off = 0b10000000
    white_dim =  0b10010101
    white_medium =  0b10101010
    white_bright =  0b10111111
    white =  0b10101010
    red_dim =  0b10000001
    red_medium =  0b10000010
    red_bright =  0b10000011
    red =  red_medium
    green_dim =  0b10000100
    green_medium =  0b10001000
    green_bright =  0b10001100
    green =  0b10001000
    blue_dim =  0b10010000
    blue_medium =  0b10100000
    blue_bright =  0b10110000
    blue =  0b10100000
    yellow_dim =  0b10000101
    yellow_medium =  0b10001010
    yellow_bright =  0b10001111
    yellow =  0b10001010
    magenta_dim =  0b10010001
    magenta_medium =  0b10100010
    magenta_bright =  0b10110011
    magenta =  0b10100010
    cyan_dim =  0b10010100
    cyan_medium =  0b10101000
    cyan_bright =  0b10111100
    cyan =  0b10101000
    orange =  0b10001011
    salmon =  0b10011011
    red_orange =  0b10000111
    red_pink =  0b10010011
    pink =  0b10100111
    purple =  0b10110010
    indigo =  0b10100001
    light_blue =  0b10111010
    lime_green =  0b10001110
    
    @classmethod
    def getValue( self, cname ):
        for name, value in self.__dict__.iteritems():
            if name == cname:
                return value
    

class LedNames:
    grip = [ 'S1', 'S2', 'S3', 'S4', 'S5', 'H1', 'H2', 'H3', 'H4' ]
    panel1 = [ 'B10', 'B11', 'B12', 'B7', 'B8', 'B9', 'B6', 'B4', 'B2', 'B5', 'B3', 'B1' ]
    panel2 = [
            'B2', 'B1', 'B4', 'B3',
            'GearUpNose', 'GearIndicator', 'GearUpLeft',
            'GearDownLeft', 'GearDownNose', 'GearDownRight',
            'GearUpRight',
            'B10', 'B8', 'B6', 'B9', 'B7', 'B5' ]
    
    @classmethod
    def getLedNumber(self, led_name, led_device):
		for i in range( 0, len(led_device)-1 ):
			if led_name == led_device[i]:
				return i
				break
    
