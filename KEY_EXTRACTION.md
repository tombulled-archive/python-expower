# python-expower: Key Extraction

## Tutorial on how to extract:
* **Device Host**
* **Device ID**
* **Device Local Key**

### What you will need:
1. An Expower Bulb
2. An Android Phone

### Step 1:
1. Download "Smart Life": https://play.google.com/store/apps/details?id=com.tuya.smartlife
2. Login/Register
3. Follow instruction and get the Bulb on your network
4. Test it is working correctly
5. Keep this app open in the background

### Step 2:
1. Download "SSL Capture": https://play.google.com/store/apps/details?id=com.minhui.networkcapture
2. Click the "two squares" in the top-left corner of the screen
3. Click "Selected App:"
4. Type "Smart Life"
5. Select "Smart Life (com.tuya.smartlife)"
6. Click the "Back arrow"
7. Click the "Green triangle" in the top-right corner of the screen (this will start intercepting packets)

### Step 3:
1. Switch application back to "Smart Life"
2. Play with some of the options available for a bit (e.g. switch between different scenes, change some values)

### Step 4:
1. Switch application back to "SSL Capture"
2. Look for an entry with approximately 16kb (If there isn't one, pick the largest one)
3. Click it
4. In the GET parameters of the first POST request, look for `deviceId=`
5. **That value is your Device Id**

### Step 5:
1. Scroll down until you find a huge JSON array (it will probably start: {"result":[{"result":{},"a":"tuya.m.my.group.device.relation.list", ...)
2. Look very carefully for: `"localKey":` (it will be there somewhere! - *Note: You want the first localKey, not the second*)
3. **That value is your Device Local Key**

### Step 6:
If you see a local IP address in the captured packets, this is the IP address of the Bulb (host)

If you don't, either:
1. Download Nmap, then portscan (Bulbs use port 6668), look for a hostname which starts with ESP
2. Use your Routers web-interface (if it has one), look for a device name starting with ESP
