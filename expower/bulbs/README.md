# python-expower: expower.bulbs

### Example: bulbs
```python
>>> import expower
>>> from pprint import pprint
>>> 
>>> # Bulb information
>>> DEVICE_ID = '<<DeviceId>>'
>>> HOST = '<<Host>>'
>>> LOCAL_KEY = '<<LocalKey>>'
>>> 
>>> # Create a <BulbDevice> instance
>>> bulb_device = expower.BulbDevice(DEVICE_ID, HOST, LOCAL_KEY)
>>> bulb_device
<BulbDevice(tcp://<<Host>>:6668)[device_id=<<DeviceId>>,local_key=<<LocalKey>>]>
>>>
>>> # Check it's working
>>> bulb_device.get_brightness()
100
>>>
>>> # Create a <Bulb> instance
>>> bulb = expower.BulbDevice(DEVICE_ID, HOST, LOCAL_KEY)
>>> bulb
<BulbDevice(tcp://<<Host>>:6668)[device_id=<<DeviceId>>,local_key=<<LocalKey>>]>
>>>
>>> # Check it's working
>>> bulb_device.get_colour()
(50, 45, 37)
>>> 
```
