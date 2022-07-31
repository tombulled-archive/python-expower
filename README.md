# python-expower
Python 3 API for Expower Smart Bulbs

<p align="center">
    <img src="https://www.androidcentral.com/sites/androidcentral.com/files/article_images/2018/12/lohas-smart-led-bulb-render.png" alt="Expower Smart Wifi B22 Rgb Dimmable 7W LED Bulb" width="200px">
</p>

## Tested Bulbs
| Bulb                                            | Link                                                  |
| ----------------------------------------------- | ----------------------------------------------------- |
| Expower Smart Wifi B22 Rgb Dimmable 7W LED Bulb | http://www.iexpower.com/en/h_product_1482156406183304 |

## Getting Started
You must first find some values identifying your Smart Bulb

Follow this tutorial: https://github.com/tombulled/python-expower/blob/master/KEY_EXTRACTION.md

If that doesn't help, see: https://github.com/clach04/python-tuya/wiki

## Example Usage
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
>>> _ = bulb.set_colour(50, 45, 37) # RGB values
>>> 
>>> # Get funky
>>> _ = bulb.set_wonderful()
>>> _ = bulb.edit_wonderful(speed=100)
>>> 
```