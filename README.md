hueapi
======

Python library for interacting with the Philips Hue lighting system

Usage
-----
```python
from hue import Hue

h = Hue("192.168.0.2", "182012820417asdf1801208")

h.toggle_light(1, False) # Switch off light 1

h.set_light(1, "#FF0000", 150) # Set light 1 to red at 150/255 brightness
```
