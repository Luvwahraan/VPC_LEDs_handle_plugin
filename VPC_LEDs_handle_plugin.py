import hid
import numpy

import traceback


VPC_left = hid.enumerate(vendor_id=0x3344, product_id=0x0137)
VPC_left = VPC_left[len(VPC_left)-1]['path']

VPC_right = hid.enumerate(vendor_id=0x3344, product_id=0xC138)
VPC_right = VPC_right[len(VPC_right)-1]['path']

BLANK = 0x0


# Commands
# SET_ADD_ON_GRIPS_LEDS = 0x65       # 101 - Add-on grips (1-4)
# SET_ON_BOARD_LEDS = 0x66           # 102 − On-board LEDs (1-20)
# SET_SLAVE_BOARD_LEDS = 0x67        # 103 − Slave-device LEDs (1-20)
# SET_EXTRA_LEDS = 0x68              # 104 − Extra LEDs (Constellation Alpha Prime 1-9)
# SECONDARY = 0x00


led_bank = numpy.full( 32, 0b01100000, dtype=numpy.uint8)
#led_bank = numpy.full( 32, 0, dtype=numpy.uint8)

panelReport = numpy.insert( led_bank, 0, 
        numpy.array([0x2, 0x67, BLANK, BLANK, BLANK], dtype=numpy.uint8) )
panelReport = numpy.append( panelReport, 
        numpy.array([0xF0], dtype=numpy.uint8) )

VPC_joys = { VPC_left: hid.device(), VPC_right: hid.device() }


for [key, value] in VPC_joys.items():
    try:
        hidraw = value
        hidraw.open_path(key)
        hidraw.set_nonblocking(1)

        ret = hidraw.send_feature_report( panelReport )
        
        if ret != 1:
            print( hidraw.error() )
        else:
            print( ret )
    except:
        print(traceback.format_exc())
