# Not perfect, but it works.

In progress… slowly. I really don’t know python. :p


## Limitations

- When firmware change a LED status, all not firmware defined LED resets to firmware status.
- Does not make coffee. (-:
- Joystick Gremlin does not want hidapi to work (cython stuff problem?).
- Designed for my specific config and hardware, for [Star Citizen](https://github.com/Luvwahraan/SC-Configs).


## How it works

In `VPC_LEDs_handle_plugin.py` file there is a dictionnary (`BUTTONS`) who associates LED objects, buttons and colors.
Just add data the correct way.

Next you need to create a callback in this file for each button.
You can do that by hand, but function `generateButtonEvents()` can generates that in Joystick Gremlin's log, so you can copy/paste the result, and removing dates.
Maybe I will automatize that, but not for now.


## That’s a JG plugin

Another [Joystick Gremlin](https://github.com/WhiteMagic/JoystickGremlin) plugin, to handle Virpils's LEDs.


## Thanks

Thanks to [ryanwoodcox](https://github.com/ryanwoodcox), who shows led HID exemples,
in [node-virpil-leds repository](https://github.com/ryanwoodcox/node-virpil-leds).
Thanks too to [charliefoxtwo], for same reason: [virpilLeds.md ](https://gist.github.com/charliefoxtwo/d294636e322402d1ea4a0f7b7e8aa52c)


# ToDO

- Fix and complete colors
- A better way to kill server