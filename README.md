# Doesn't work yet.

In progress… slowly. I don’t know python. :p


## What actually works
- Usb hid, with [hidapi](https://github.com/libusb/hidapi) and [cython-hidapi](https://pypi.org/project/hidapi/).
- LED handle for Virpil, in master and slave modes
- LED names for joystick and panels
- Disco Virpil, dude!


## Limitations
- When firmware change a LED status, all not firmware defined LED resets to firmware status.
- Does not make coffee. (-:
- Joystick Gremlin does not want hidapi to work (cython stuff problem?).
I’m going use some client/server architecture to fix that, but I don’t like it.


## How it works
In `VPC_LEDs_handle_plugin.py` file there is a dictionnary (BUTTONS) who associates LEDs, buttons and colors.
Just add physical buttons numbers in right places.

Next you need to create a callback for each button.
Function `generateButtonEvents()` can generates that in Joystick Gremlin's log, so you can copy/paste the result, and removing dates.


## This tends to become a plugin.
Another [Joystick Gremlin](https://github.com/WhiteMagic/JoystickGremlin) plugin, to handle Virpils's LEDs.


## Thanks to ryanwoodcox.
Thanks to [ryanwoodcox](https://github.com/ryanwoodcox), who shows led HID exemples,
in [node-virpil-leds repository](https://github.com/ryanwoodcox/node-virpil-leds).
Thanks too to [charliefoxtwo], for same reason: [virpilLeds.md](https://gist.github.com/charliefoxtwo/d294636e322402d1ea4a0f7b7e8aa52c)


# ToDO

- Fix and complete colors
- A better way to kill server
- Describe how it works