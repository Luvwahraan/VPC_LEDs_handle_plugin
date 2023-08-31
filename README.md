# Doesn't work yet.
In progress… slowly. I don’t know python. :p

## What actually works
- Usb hid, with [hidapi](https://github.com/libusb/hidapi) and [cython-hidapi](https://pypi.org/project/hidapi/).
- LED handle for Virpil, in master and slave modes
- LED names for joystick and panels

## Limitations
- When firmware change a LED status, all not firmware defined LED resets to firmware status.
- Does not make coffee. (-:
- Changing too quickly and/or many time seems to freeze LEDs.

## This tends to become a plugin.
Another [Joystick Gremlin plugin](https://github.com/WhiteMagic/JoystickGremlin), to handle Virpils's LEDs.


## Thanks to ryanwoodcox.
Thanks to [ryanwoodcox](https://github.com/ryanwoodcox), who shows led HID exemples,
in [node-virpil-leds repository](https://github.com/ryanwoodcox/node-virpil-leds).
