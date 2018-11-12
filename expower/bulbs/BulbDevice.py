from .. import pytuya
from .. import constants
from .. import utils
from . import decorators

"""
Imports:
    ..pytuya
    ..constants
    ..utils
    .decorators

Contains:
    <BulbDevice>
"""

class BulbDevice(pytuya.BulbDevice):
    """
    Inherits from pytuya.BulbDevice

    Tailored to Expower Bulbs, with some improvements
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise self and super

        :param *args - *args to be passed to <pytuya.BulbDevice>.__init__
        :param *args - *args to be passed to <pytuya.BulbDevice>.__init__

        :returns - None
        """

        self._init_attrs()

        super().__init__(*args, **kwargs)

        self.host = self.address
        self.device_id = self.id

    def __repr__(self):
        """
        Returns a string representation of the object
        ... in the form:
            <class_name(tcp://host:port)[device_id=...,local_key=...]>
        """

        data = \
        (
            '<'
                f'{self.__class__.__name__}'
                '('
                    f'{self.protocol}://{self.host}:{self.port}'
                ')'
                '['
                    f'device_id={self.device_id},'
                    f'local_key={self.local_key.decode()}'
                ']'
            '>'
        )

        return data

    def get_brightness(self, state=None):
        """
        Get the current brightness level

        :param state - Pre-captured self.state() data
            ... E.g:
            ... state = bulb.state()
            ... brightness = bulb.get_brightness(state = state)

        :returns(int) - brightness (%)

        Note: This value is only used by 'white' mode
        """

        if state is None:
            state = self.state()

        brightness = state.get(constants.state_keys.BRIGHTNESS, None)

        return brightness

    def get_colour(self, state=None):
        """
        Get the current colour (as RGB)

        :param state - Pre-captured self.state() data
            ... E.g:
            ... state = bulb.state()
            ... brightness = bulb.get_colour(state = state)

        :returns(tuple) - Colour as (r, g, b)

        Note: This value is only used by 'colour' mode
        """

        if state is None:
            state = self.state()

        colour = state.get(constants.state_keys.COLOUR, None)

        return colour

    def get_temperature(self, state=None):
        """
        Get the current colour temperature

        :param state - Pre-captured self.state() data
            ... E.g:
            ... state = bulb.state()
            ... brightness = bulb.get_temperature(state = state)

        :returns(int) - Temperature (%)

        Note: This value is only used by 'colour' mode
        Note: This is NOT temperature as in heat
        """

        if state is None:
            state = self.state()

        temperature = state.get(constants.state_keys.TEMPERATURE, None)

        return temperature

    def set_colour(self, r=None, g=None, b=None):
        """
        Set the Bulb's colour (RGB)

        :param(int) r - Red (0 to 255)
            ... OR, tuple/list of (r, g, b)
        :param(int) g - Green (0 to 255)
        :param(int) b - Blue (0 to 255)

        :returns(bytes) - Bulb response

        E.g:
            >>> # Example use 1:
            >>> bulb.set_colour(0, 255, 255)
            >>> # Example use 2:
            >>> bulb.set_colour((0, 255, 255))

        Note: This value is only used by 'colour' mode
        """

        if isinstance(r, tuple) or isinstance(r, list):
            r, g, b, *_ = r

        rgb = (r, g, b)

        if any(colour is None for colour in rgb):
            return

        return super().set_colour(*rgb)

    def set_temperature(self, temperature):
        """
        Set the Bulb's (colour) temperature

        :param(int) temperature - Colour temperature (%)

        :returns(bytes) - Bulb response

        Note: This value is only used by 'white' mode
        Note: This is NOT temperature as in heat
        """

        return super().set_colourtemp(temperature)

    def set_brightness(self, brightness):
        """
        Set the Bulb's brightness

        :param(int) brightness - Brightness (%)

        :returns(bytes) - Bulb response

        Note: This value is only used by 'white' mode
        """

        return super().set_brightness(brightness)

    def set_white(self, brightness=None, temperature=None):
        """
        Set the Bulb to 'white' mode

        :param(int) brightness - Brightness (%)
        :param(int) temperature - Colour temperature (%)

        :returns(bytes) - Bulb response
        """

        state = self.state()

        if brightness is None:
            brightness = state[constants.state_keys.BRIGHTNESS]
        if temperature is None:
            temperature = state[constants.state_keys.TEMPERATURE]

        return super().set_white(brightness, temperature)

    def set_scene(self, scene=0):
        """
        Set the Blub to scene {scene}

        :param(int) scene - Scene index (0 to 4)

        :returns(bytes) - Bulb response
        """

        if scene < 0 or scene > 4:
            return

        scene_id = constants.schema_keys.SCENE

        if scene > 0:
            scene_id += f'_{scene}'

        payload = self.generate_payload \
        (
            pytuya.SET,
            {
                self.DPS_INDEX_MODE: scene_id,
            }
        )

        data = self._send_receive(payload)

        return data

    def state(self):
        """
        Get the Bulb's state as (decoded) readable values

        :returns(dict) - Bulb state

        Example output:
            {'brightness': 100,
             'colour': (50, 10, 50),
             'mode': 'white',
             'on': True,
             'scene': (56, 85, 180),
             'scenes': {'colourful': {'brightness': 41,
                                      'colours': [(105, 38, 38),
                                                  (105, 93, 38),
                                                  (38, 105, 38),
                                                  (38, 98, 105),
                                                  (51, 38, 105),
                                                  (105, 38, 97)],
                                      'saturation': 64,
                                      'speed': 100},
                        'exciting': {'brightness': 10,
                                     'colour': (0, 0, 255),
                                     'saturation': 0,
                                     'speed': 100},
                        'soft': {'brightness': 4,
                                 'colour': (255, 0, 0),
                                 'saturation': 80,
                                 'speed': 100},
                        'wonderful': {'brightness': 100,
                                      'colours': [(255, 0, 0),
                                                  (255, 230, 0),
                                                  (9, 255, 0),
                                                  (0, 247, 255),
                                                  (255, 255, 255),
                                                  (247, 0, 255)],
                                      'saturation': 100,
                                      'speed': 100}},
             'temperature': 100}
        """

        schema = self.schema()

        if not schema:
            return {}

        state = {}

        for state_key in constants.state_keys.STATE_KEYS:
            if state_key == constants.state_keys.SCENES:
                continue

            schema_key = constants.maps.STATE_KEY_TO_SCHEMA_KEY[state_key]

            value = schema.get(schema_key, None)

            state[state_key] = value

        if state.get(constants.state_keys.COLOUR, None) is not None:
            state[constants.state_keys.COLOUR] = self._hexvalue_to_rgb \
            (
                state[constants.state_keys.COLOUR]
            )
        if state.get(constants.state_keys.SCENE, None) is not None:
            state[constants.state_keys.SCENE] = self._hexvalue_to_rgb \
            (
                state[constants.state_keys.SCENE]
            )

        state[constants.state_keys.SCENES] = {}

        flash_scenes = schema.get(constants.schema_keys.FLASH_SCENES, ())

        for index, flash_scene in enumerate(flash_scenes):
            flash_scene_name = constants.schema_keys.FLASH_SCENES_LIST[index]

            if flash_scene is not None:
                decoder = self._map_flash_scene_to_decoder[flash_scene_name]

                decoded_flash_scene = decoder(flash_scene)
            else:
                decoded_flash_scene = None

            scene_key = constants.maps.FLASH_SCENE_TO_SCENE[flash_scene_name]
            scene_name = constants.maps.SCENE_TO_NAME[scene_key]

            state[constants.state_keys.SCENES][scene_name] = decoded_flash_scene

        return state

    def schema(self):
        """
        Returns the Bulb's status formatted with schema keys

        :returns(dict) - Bulb status as schema

        Example output:
            {'bright_value': 100,
             'colour_data': '320a32012ccc32',
             'flash_scenes': ['24d10101ff0000',
                              '78ac0106692626695d26266926266269332669692661',
                              '311b0101ff0000',
                              'ffff0106ff0000ffe60009ff0000f7fffffffff700ff'],
             'led_switch': True,
             'scene_data': '3855b40168ffff',
             'temp_value': 100,
             'work_mode': 'white'}

        Note: values are not decoded
        """

        status = self.status()

        if not status:
            return {}

        dps = status.get(constants.status_keys.DPS, ())

        dps_index_map = {index: val for index, val in enumerate(dps)}

        schema = {}

        for schema_key, index in constants.maps.SCHEMA_KEY_TO_DPS_INDEX.items():
            schema[schema_key] = dps_index_map[index]

        schema[constants.schema_keys.FLASH_SCENES] = []

        for FLASH_SCENE in constants.schema_keys.FLASH_SCENES_LIST:
            flash_scene = schema.get(FLASH_SCENE, None)

            if flash_scene is not None:
                schema[constants.schema_keys.FLASH_SCENES].append(flash_scene)

                del schema[FLASH_SCENE]

        return schema

    def status(self):
        """
        Get Bulb's status: Raw status (not decoded or formatted)

        :returns(dict) - Bulb's status

        Example output:
            {'device_id': '<<REDACTED>>',
             'dps': [True,
                     'white',
                     100,
                     100,
                     '320a32012ccc32',
                     '3855b40168ffff',
                     '24d10101ff0000',
                     '78ac0106692626695d26266926266269332669692661',
                     '311b0101ff0000',
                     'ffff0106ff0000ffe60009ff0000f7fffffffff700ff']}
        """

        super_status = super().status()

        if not super_status:
            return {}

        device_id = super_status.get(constants.status_keys.DEV_ID, None)
        dps = super_status.get(constants.status_keys.DPS, {})

        dps =  \
        {
            int(key) - 1: val \
                for key, val in dps.items() \
                    if \
                    (
                        isinstance(key, str) \
                        and key.isdigit() \
                    ) \
                        or isinstance(key, int) \
        }

        dps_list = []

        for key in sorted(dps.keys()):
            if key == len(dps_list):
                dps_list.append(dps[key])
            elif key > 0:
                for index in range(len(dps_list), key):
                    dps_list.append(None)

                dps_list.append(dps[key])

        status = \
        {
            constants.status_keys.DEVICE_ID: device_id,
            constants.status_keys.DPS: dps_list,
        }

        return status

    def edit_soft \
            (
                self,
                saturation = None,
                brightness = None,
                speed = None,
                colour = None,
            ):
        """
        Edit the soft scene

        :param(int) saturation - Saturation (%)
        :param(int) brightness - Brightness (%)
        :param(int) speed - Speed (%)
        :param(tuple[int]) colour - RGB Colour as (r, g, b)

        :returns(bytes) - Bulb response

        Note: Only use to set colour and speed
        """

        state = self.state()

        scenes = state[constants.state_keys.SCENES]

        scene_id = constants.schema_keys.SCENE_1
        flash_scene_id = constants.schema_keys.FLASH_SCENE_1

        scene_name = constants.maps.SCENE_TO_NAME[scene_id]
        scene_index = constants.maps.SCENE_TO_INDEX[scene_name]

        flash_scene_index = constants.maps.SCHEMA_KEY_TO_DPS_INDEX[flash_scene_id]
        str_flash_scene_index = str(flash_scene_index + 1)

        scene = scenes[scene_name]

        if saturation is None:
            saturation = scene[constants.state_keys.SATURATION]
        if brightness is None:
            brightness = scene[constants.state_keys.BRIGHTNESS]
        if speed is None:
            speed = scene[constants.state_keys.SPEED]
        if colour is None:
            colour = scene[constants.state_keys.COLOUR]

        int_saturation = self._saturation_to_hexvalue(saturation)
        int_brightness = self._brightness_to_hexvalue(brightness)
        int_speed = self._speed_to_hexvalue(speed)

        hex_saturation = utils.int_to_hex(int_saturation)
        hex_brightness = utils.int_to_hex(int_brightness)
        hex_speed = utils.int_to_hex(int_speed)

        hex_colour = super()._rgb_to_hexvalue(*colour)[:6] # Only get rgb

        hexvalue = f'{hex_brightness}{hex_saturation}{hex_speed}01{hex_colour}'

        payload = super().generate_payload(pytuya.SET, {str_flash_scene_index: hexvalue})

        data = super()._send_receive(payload)

        return data

    def edit_colourful \
            (
                self,
                saturation = None,
                brightness = None,
                speed = None,
                colours = (),
            ):
        """
        Edit the colourful scene

        :param(int) saturation - Saturation (%)
        :param(int) brightness - Brightness (%)
        :param(int) speed - Speed (%)
        :param(tuple[tuple[int]]) colours - Tuple of RGB Colours as (r, g, b)
            ... OR dict of {index: colour}
                ... WHERE index is 1-based

        :returns(bytes) - Bulb response

        Note: Only use to set colours and speed
        """

        state = self.state()

        scenes = state[constants.state_keys.SCENES]

        scene_id = constants.schema_keys.SCENE_2
        flash_scene_id = constants.schema_keys.FLASH_SCENE_2

        scene_name = constants.maps.SCENE_TO_NAME[scene_id]
        scene_index = constants.maps.SCENE_TO_INDEX[scene_name]

        flash_scene_index = constants.maps.SCHEMA_KEY_TO_DPS_INDEX[flash_scene_id]
        str_flash_scene_index = str(flash_scene_index + 1)

        scene = scenes[scene_name]

        if saturation is None:
            saturation = scene[constants.state_keys.SATURATION]
        if brightness is None:
            brightness = scene[constants.state_keys.BRIGHTNESS]
        if speed is None:
            speed = scene[constants.state_keys.SPEED]

        int_saturation = self._saturation_to_hexvalue(saturation)
        int_brightness = self._brightness_to_hexvalue(brightness)
        int_speed = self._speed_to_hexvalue(speed)

        hex_saturation = utils.int_to_hex(int_saturation)
        hex_brightness = utils.int_to_hex(int_brightness)
        hex_speed = utils.int_to_hex(int_speed)

        colours_hexvalues = []

        pre_colours = scene[constants.state_keys.COLOURS]

        for index in range(len(pre_colours)):
            colour_hexvalue = super()._rgb_to_hexvalue(*pre_colours[index])[:6] # Only get rgb

            colours_hexvalues.append(colour_hexvalue)

        if isinstance(colours, list) or isinstance(colours, tuple):
            colours = {index + 1: colour for index, colour in enumerate(colours)}

        for index, colour_rgb in colours.items():
            if isinstance(index, str) and index.isdigit():
                index = int(index)
            elif not isinstance(index, int):
                continue

            index -= 1

            colour_hexvalue = super()._rgb_to_hexvalue(*colour_rgb)[:6]

            colours_hexvalues[index] = colour_hexvalue

        colours_hexvalue = ''.join(colours_hexvalues)

        hexvalue = f'{hex_brightness}{hex_saturation}{hex_speed}06{colours_hexvalue}'

        payload = super().generate_payload(pytuya.SET, {str_flash_scene_index: hexvalue})

        data = super()._send_receive(payload)

        return data

    def edit_exciting \
            (
                self,
                saturation = None,
                brightness = None,
                speed = None,
                colour = None,
            ):
        """
        Edit the exciting scene

        :param(int) saturation - Saturation (%)
        :param(int) brightness - Brightness (%)
        :param(int) speed - Speed (%)
        :param(tuple[int]) colour - RGB Colour as (r, g, b)

        :returns(bytes) - Bulb response

        Note: Only use to set colour and speed
        """

        state = self.state()

        scenes = state[constants.state_keys.SCENES]

        scene_id = constants.schema_keys.SCENE_3
        flash_scene_id = constants.schema_keys.FLASH_SCENE_3

        scene_name = constants.maps.SCENE_TO_NAME[scene_id]
        scene_index = constants.maps.SCENE_TO_INDEX[scene_name]

        flash_scene_index = constants.maps.SCHEMA_KEY_TO_DPS_INDEX[flash_scene_id]
        str_flash_scene_index = str(flash_scene_index + 1)

        scene = scenes[scene_name]

        if saturation is None:
            saturation = scene[constants.state_keys.SATURATION]
        if brightness is None:
            brightness = scene[constants.state_keys.BRIGHTNESS]
        if speed is None:
            speed = scene[constants.state_keys.SPEED]
        if colour is None:
            colour = scene[constants.state_keys.COLOUR]

        int_saturation = self._saturation_to_hexvalue(saturation)
        int_brightness = self._brightness_to_hexvalue(brightness)
        int_speed = self._speed_to_hexvalue(speed)

        hex_saturation = utils.int_to_hex(int_saturation)
        hex_brightness = utils.int_to_hex(int_brightness)
        hex_speed = utils.int_to_hex(int_speed)

        # colour = colour[::-1] ## Why is this not flipped here, but is in decoding???

        hex_colour = super()._rgb_to_hexvalue(*colour)[:6] # Only rgb

        hexvalue = f'{hex_brightness}{hex_saturation}{hex_speed}01{hex_colour}'

        payload = super().generate_payload(pytuya.SET, {str_flash_scene_index: hexvalue})

        data = super()._send_receive(payload)

        return data

    def edit_wonderful \
            (
                self,
                saturation = None,
                brightness = None,
                speed = None,
                colours = (),
            ):
        """
        Edit the wonderful scene

        :param(int) saturation - Saturation (%)
        :param(int) brightness - Brightness (%)
        :param(int) speed - Speed (%)
        :param(tuple[tuple[int]]) colours - Tuple of RGB Colours as (r, g, b)
            ... OR dict of {index: colour}
                ... WHERE index is 1-based

        :returns(bytes) - Bulb response

        Note: Only use to set colours and speed
        """

        state = self.state()

        scenes = state[constants.state_keys.SCENES]

        scene_id = constants.schema_keys.SCENE_4
        flash_scene_id = constants.schema_keys.FLASH_SCENE_4

        scene_name = constants.maps.SCENE_TO_NAME[scene_id]
        scene_index = constants.maps.SCENE_TO_INDEX[scene_name]

        flash_scene_index = constants.maps.SCHEMA_KEY_TO_DPS_INDEX[flash_scene_id]
        str_flash_scene_index = str(flash_scene_index + 1)

        scene = scenes[scene_name]

        if saturation is None:
            saturation = scene[constants.state_keys.SATURATION]
        if brightness is None:
            brightness = scene[constants.state_keys.BRIGHTNESS]
        if speed is None:
            speed = scene[constants.state_keys.SPEED]

        int_saturation = self._saturation_to_hexvalue(saturation)
        int_brightness = self._brightness_to_hexvalue(brightness)
        int_speed = self._speed_to_hexvalue(speed)

        hex_saturation = utils.int_to_hex(int_saturation)
        hex_brightness = utils.int_to_hex(int_brightness)
        hex_speed = utils.int_to_hex(int_speed)

        colours_hexvalues = []

        pre_colours = scene[constants.state_keys.COLOURS]

        for index in range(len(pre_colours)):
            colour_hexvalue = super()._rgb_to_hexvalue(*pre_colours[index])[:6] # Only get rgb

            colours_hexvalues.append(colour_hexvalue)

        if isinstance(colours, list) or isinstance(colours, tuple):
            colours = {index + 1: colour for index, colour in enumerate(colours)}

        for index, colour_rgb in colours.items():
            if isinstance(index, str) and index.isdigit():
                index = int(index)
            elif not isinstance(index, int):
                continue

            index -= 1

            colour_hexvalue = super()._rgb_to_hexvalue(*colour_rgb)[:6] # Only get RGB

            colours_hexvalues[index] = colour_hexvalue

        colours_hexvalue = ''.join(colours_hexvalues)

        hexvalue = f'{hex_brightness}{hex_saturation}{hex_speed}06{colours_hexvalue}'

        payload = super().generate_payload(pytuya.SET, {str_flash_scene_index: hexvalue})

        data = super()._send_receive(payload)

        return data

    def _decode_flash_scene_1(self, hexvalue):
        """
        Decode flash_scene_1's hexvalue

        :param(str) hexvalue - flash_scene_1's hexvalue

        Uses: self._decode_one_colour_flash_scene
        """

        return self._decode_one_colour_flash_scene(hexvalue)

    def _decode_flash_scene_2(self, hexvalue):
        """
        Decode flash_scene_2's hexvalue

        :param(str) hexvalue - flash_scene_2's hexvalue

        Uses: self._decode_six_colour_flash_scene
        """

        return self._decode_six_colour_flash_scene(hexvalue)

    def _decode_flash_scene_3(self, hexvalue):
        """
        Decode flash_scene_3's hexvalue

        :param(str) hexvalue - flash_scene_3's hexvalue

        Uses: self._decode_one_colour_flash_scene_flipped
        """

        return self._decode_one_colour_flash_scene_flipped(hexvalue)

    def _decode_flash_scene_4(self, hexvalue):
        """
        Decode flash_scene_4's hexvalue

        :param(str) hexvalue - flash_scene_4's hexvalue

        Uses: self._decode_six_colour_flash_scene
        """

        return self._decode_six_colour_flash_scene(hexvalue)

    def _decode_one_colour_flash_scene(self, hexvalue):
        """
        Decodes {hexvalue} into a dictionary

        :param(str) hexvalue - Flash Scene hexvalue (short one)

        :returns(dict) - Decoded {hexvalue} values

        hexvalue Format: {br}{sa}{sp}[01]{co}
            {br} -> brightness
            {sa} -> saturation
            {sp} -> speed
            [01] -> unused
            {co} -> colour
                ... -> {rr}{gg}{bb}

            Where:
                {rr} -> red
                {gg} -> green
                {bb} -> blue
        """

        if len(hexvalue) != 14:
            return {}

        br, sa, sp, _01, rr, gg, bb = utils.chunk(hexvalue, 2)

        red = utils.hex_to_int(rr)
        green = utils.hex_to_int(gg)
        blue = utils.hex_to_int(bb)

        rgb = (red, green, blue)

        speed = self._hexvalue_to_speed(utils.hex_to_int(sp))

        brightness = self._hexvalue_to_brightness(utils.hex_to_int(br))

        saturation = self._hexvalue_to_saturation(utils.hex_to_int(sa))

        data = \
        {
            constants.state_keys.COLOUR: rgb,
            constants.state_keys.SPEED: speed,
            constants.state_keys.BRIGHTNESS: brightness,
            constants.state_keys.SATURATION: saturation,
        }

        return data

    def _decode_one_colour_flash_scene_flipped(self, hexvalue):
        """
        Decodes {hexvalue} into a dictionary

        :param(str) hexvalue - Flash Scene hexvalue (short one)
            ... For some reason rgb is in reverse order

        :returns(dict) - Decoded {hexvalue} values

        Format: {br}{sa}{sp}[01]{co}
            {br} -> brightness
            {sa} -> saturation
            {sp} -> speed
            [01] -> unused
            {co} -> colour
                ... -> {bb}{gg}{rr}

            Where:
                {rr} -> red
                {gg} -> green
                {bb} -> blue
        """

        if len(hexvalue) != 14:
            return {}

        br, sa, sp, _01, bb, gg, rr = utils.chunk(hexvalue, 2)

        red = utils.hex_to_int(rr)
        green = utils.hex_to_int(gg)
        blue = utils.hex_to_int(bb)

        rgb = (red, green, blue)

        speed = self._hexvalue_to_speed(utils.hex_to_int(sp))

        brightness = self._hexvalue_to_brightness(utils.hex_to_int(br))

        saturation = self._hexvalue_to_saturation(utils.hex_to_int(sa))

        data = \
        {
            constants.state_keys.COLOUR: rgb,
            constants.state_keys.SPEED: speed,
            constants.state_keys.BRIGHTNESS: brightness,
            constants.state_keys.SATURATION: saturation,
        }

        return data

    def _decode_six_colour_flash_scene(self, hexvalue):
        """
        Decodes {hexvalue} into a dictionary

        :param(str) hexvalue - Flash Scene hexvalue (long one)

        :returns(dict) - Decoded {hexvalue} values

        Format: {br}{sa}{sp}[06]{c1}{c2}{c3}{c4}{c5}{c6}
            {br} -> brightness
            {sa} -> saturation
            {sp} -> speed
            [06] -> unused
            {c1} -> colour 1
                ... -> {rr}{gg}{bb}
            {c2} -> colour 2
                ... -> {rr}{gg}{bb}
            {c3} -> colour 3
                ... -> {rr}{gg}{bb}
            {c4} -> colour 4
                ... -> {rr}{gg}{bb}
            {c5} -> colour 5
                ... -> {rr}{gg}{bb}
            {c6} -> colour 6
                ... -> {rr}{gg}{bb}

            Where:
                {rr} -> red
                {gg} -> green
                {bb} -> blue

        On device screen, colours are in order (relative to hexvalue):
            1 2 3
            4 5 6
        """

        if len(hexvalue) != 44:
            return {}

        hex_values = utils.chunk(hexvalue, 2)

        br, sa, sp, _06, *cs = hex_values

        brightness = self._hexvalue_to_brightness(utils.hex_to_int(br))

        saturation = self._hexvalue_to_saturation(utils.hex_to_int(sa))

        speed = self._hexvalue_to_speed(utils.hex_to_int(sp))

        colours = []

        for cn in utils.chunk(cs, 3):
            if len(cn) != 3:
                continue

            rr, gg, bb = cn

            red = utils.hex_to_int(rr)
            green = utils.hex_to_int(gg)
            blue = utils.hex_to_int(bb)

            rgb = (red, green, blue)

            colours.append(rgb)

        data = \
        {
            constants.state_keys.SPEED: speed,
            constants.state_keys.BRIGHTNESS: brightness,
            constants.state_keys.SATURATION: saturation,
            constants.state_keys.COLOURS: colours,
        }

        return data

    def _brightness_to_hexvalue(self, brightness, u=26.9):
        """
        Convert {brightness} (%) to an integer used
        ... by the Bulb

        :param(int) brightness - Brightness (%)
        :param(float) u - Brightness encoding offset
            ... Recommended to leave this as-is

        :returns(int) - Hexvalue used by the Bulb

        Note: This method was entirely brute-forced and bodged
            ... This needs to be reviewed
            ... I have no idea why values are encoded like this
            ... But ~27 seemed to work
        """

        brightness = self._in_range(brightness, min = 0, max = 100)

        hexvalue = int(u + ((255 - u) / 100) * brightness)

        return hexvalue

    def _hexvalue_to_brightness(self, hexvalue, u=26.9):
        """
        Convert {hexvalue} to a brightness value (%)

        :param(int) hexvalue - Integer hexvalue
        :param(float) u - Brightness encoding offset
            ... Recommended to leave this as-is

        :returns(int) - Brightness (%)

        Note: This method was entirely brute-forced and bodged
            ... This needs to be reviewed
            ... I have no idea why values are encoded like this
            ... But ~27 seemed to work
        """

        brightness = int((hexvalue - u) / ((255 - u) / 100)) + 1

        brightness = self._in_range(brightness, min = 0, max = 100)

        return brightness

    def _saturation_to_hexvalue(self, saturation, u=27):
        """
        Convert {saturation} (%) to an integer used
        ... by the Bulb

        :param(int) saturation - Saturation (%)
        :param(float) u - Saturation encoding offset
            ... Recommended to leave this as-is

        :returns(int) - Hexvalue used by the Bulb

        Note: This method was entirely brute-forced and bodged
            ... This needs to be reviewed
            ... I have no idea why values are encoded like this
            ... But ~27 seemed to work
        """

        saturation = self._in_range(saturation, min = 0, max = 100)

        hexvalue = int(u + ((255 - u) / 100) * saturation + 0.00001)

        return hexvalue

    def _hexvalue_to_saturation(self, hexvalue, u=27):
        """
        Convert {hexvalue} to an integer used
        ... by the Bulb

        :param(int) hexvalue - Integer saturation hexvalue
        :param(float) u - Saturation encoding offset
            ... Recommended to leave this as-is

        :returns(int) - Saturation (%)

        Note: This method was entirely brute-forced and bodged
            ... This needs to be reviewed
            ... I have no idea why values are encoded like this
            ... But ~27 seemed to work
        """

        saturation = int((hexvalue - u) / ((255 - u) / 100) + 0.5)

        saturation = self._in_range(saturation, min = 0, max = 100)

        return saturation

    def _hexvalue_to_speed(self, hexvalue):
        """
        Convert {hexvalue} to speed (%)

        :param(int) hexvalue - Integer speed hexvalue

        :returns(int) - Speed (%)

        Note: This method was entirely brute-forced and bodged
            ... This needs to be reviewed
            ... I have no idea why values are encoded like this
            ... But this seems to work
        """

        speed = 101 - hexvalue

        speed = self._in_range(speed, min = 0, max = 100)

        return speed

    def _speed_to_hexvalue(self, speed):
        """
        Convert {speed} to an integer used
        ... by the Bulb

        :param(int) speed - Speed (%)

        :returns(int) - Hexvalue used by the Bulb

        Note: This method was entirely brute-forced and bodged
            ... This needs to be reviewed
            ... I have no idea why values are encoded like this
            ... But this seems to work
        """

        speed = self._in_range(speed, 0, 100)

        hexvalue = 101 - speed

        return hexvalue

    @decorators.on_connection_reset(None)
    def _send_receive(self, *args, **kwargs):
        """
        Wrapper for super()._send_receive

        Implements: @decorators.on_connection_reset(None)
        """

        return super()._send_receive(*args, **kwargs)

    def _super(self):
        """
        Returns super()
        """

        return super()

    def _in_range(self, value, min=0, max=100):
        """
        Make sure {value} is in range {min} to {max}

        :param(int) value - Value to be observed
        :param(int) min - If value < min: value = min
        :param(int) max - If value > max: value = max

        :returns(int) - {value} in range {min} to {max}
        """

        if value < min:
            value = min
        if value > max:
            value = max

        return value

    def _init_attrs(self):
        """
        Initialise class attributes
        """

        self.host = None
        self.port = constants.ports.PORT_BULB
        self.device_id = None
        self.local_key = None
        self.protocol = constants.protocols.TCP

        self._map_flash_scene_to_decoder = \
        {
            constants.schema_keys.FLASH_SCENE_1: self._decode_flash_scene_1,
            constants.schema_keys.FLASH_SCENE_2: self._decode_flash_scene_2,
            constants.schema_keys.FLASH_SCENE_3: self._decode_flash_scene_3,
            constants.schema_keys.FLASH_SCENE_4: self._decode_flash_scene_4,
        }
