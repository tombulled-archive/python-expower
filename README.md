# python-expower

## Python 3 API for Expower Smart Bulbs

![Expower Smart Wifi B22 Rgb Dimmable 7W LED Bulb](https://images-na.ssl-images-amazon.com/images/I/5183GmewMgL._SX500_.jpg)

-----------------------------------

### Tested on the following Bulbs:
Bulb | Link
------ | ----
Expower Smart Wifi B22 Rgb Dimmable 7W LED Bulb | https://www.amazon.co.uk/d/Colour-Changing-Bulbs/Expower-B22-7W-Compatible-Smartphone/B075Q9NHF2/

-----------------------------------

### Before you get started:
You must first find some values identifying your Smart Bulb

Follow this tutorial: https://github.com/tombulled/python-expower/blob/master/KEY_EXTRACTION.md

If that doesn't help, see: https://github.com/clach04/python-tuya/wiki

### Basic Example:
```python
>>> import expower
>>> from pprint import pprint
>>> 
>>> # Bulb information
>>> DEVICE_ID = '<<DeviceId>>'
>>> HOST = '<<BulbIP>>'
>>> LOCAL_KEY = '<<LocalKey>>'
>>> 
>>> # Create a <Bulb> instance
>>> bulb = expower.Bulb(DEVICE_ID, HOST, LOCAL_KEY)
>>> 
>>> # Get the bulb state
>>> pprint(bulb.state())
{'brightness': 100,
 'colour': (0, 255, 0),
 'mode': 'scene_4',
 'on': True,
 'scene': (56, 85, 180),
 'scenes': {'colourful': {'brightness': 41,
                          'colours': [(105, 38, 38),
                                      (0, 255, 255),
                                      (38, 105, 38),
                                      (38, 98, 105),
                                      (51, 38, 105),
                                      (105, 38, 97)],
                          'saturation': 64,
                          'speed': 10},
            'exciting': {'brightness': 10,
                         'colour': (255, 0, 0),
                         'saturation': 0,
                         'speed': 30},
            'soft': {'brightness': 4,
                     'colour': (0, 255, 0),
                     'saturation': 80,
                     'speed': 90},
            'wonderful': {'brightness': 100,
                          'colours': [(255, 0, 0),
                                      (255, 230, 0),
                                      (9, 255, 0),
                                      (0, 247, 255),
                                      (255, 255, 255),
                                      (247, 0, 255)],
                          'saturation': 100,
                          'speed': 5}},
 'temperature': 100}
>>> 
>>> # Change colour
>>> _ = bulb.set_green()
>>> _ = bulb.set_colour(50, 45, 37) # RBG values
>>> 
>>> # Get funky
>>> _ = bulb.set_wonderful()
>>> _ = bulb.edit_wonderful(speed=100)
>>> 
```

-----------------------------------

### Libraries that were of great help:

Name | Link
---- | ----
python-tuya | https://github.com/clach04/python-tuya

-----------------------------------

### Software/Applications that were of great help:

Software | Link
-------- | ----
eFamilyCloud | https://play.google.com/store/apps/details?id=com.efamily.cloud
Smart Life - Smart Living | https://play.google.com/store/apps/details?id=com.tuya.smartlife
SSL Capture | https://play.google.com/store/apps/details?id=com.minhui.networkcapture
Atom | https://atom.io/
Python | https://www.python.org/

-----------------------------------

Total bulbs harmed in the making of this code: **0**
