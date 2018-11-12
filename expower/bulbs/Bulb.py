from . import BulbDevice
from .. import constants
from .. import utils

"""
Imports:
    .BulbDevice
    ..constants
    ..utils

Contains:
    <Bulb>
"""

class Bulb(object):
    """
    Indirect wrapper for <BulbDevice>

    Picks-and-chooses what it inherits to keep
    ... the class neat and tidy
    """

    def __init__(self, *args, **kwargs):
        """
        Initialise <BulbDevice> and self

        :param *args - *args to be passed to <BulbDevice>.__init__
        :param **kwargs - **kwargs to be passed to <BulbDevice>.__init__

        :returns None
        """

        self.BulbDevice = BulbDevice(*args, **kwargs)

        for colour_name, colour_rgb in constants.rgb_colours.RGB_COLOURS.items():
            func_name = f'set_{colour_name}'

            def set_colour(colour):
                """
                Local decorator to set bulbs colour

                Level: set_colour
                """

                def wrapper():
                    """
                    Nested wrapper to call self.set_colour

                    Level: set_colour.wrapper
                    """

                    return self.set_colour(*colour)

                return wrapper

            setattr(self, func_name, set_colour(colour_rgb))

        for theme_name, theme_colour in constants.themes.THEMES.items():
            func_name = f'set_{theme_name}'

            def set_theme(colour):
                """
                Local decorator to set bulbs colour

                Level: set_theme
                """

                def wrapper():
                    """
                    Nested wrapper to call self.set_colour

                    Level: set_theme.wrapper
                    """

                    return self.set_colour(*colour)

                return wrapper

            setattr(self, func_name, set_theme(theme_colour))

        for scene_name in constants.scenes.SCENES:
            scene_index = constants.maps.SCENE_TO_INDEX[scene_name]

            func_name = f'set_{scene_name}'

            def set_scene(index):
                """
                Local decorator to set bulb scene

                Level: set_scene
                """

                def wrapper():
                    """
                    Nested wrapper to call self.set_theme

                    Level: set_scene.wrapper
                    """

                    return self.set_scene(index)

                return wrapper

            setattr(self, func_name, set_scene(scene_index))

        utils.implicitly_inherit \
        (
            src = self.BulbDevice,
            dst = self,
            attrs = \
            (
                'device_id',
                'get_brightness',
                'get_colour',
                'get_temperature',
                'host',
                'local_key',
                'port',
                'set_brightness',
                'set_colour',
                'set_temperature',
                'set_white',
                'set_scene',
                'state',
                'status',
                'schema',
                'turn_on',
                'turn_off',
                'edit_soft',
                'edit_colourful',
                'edit_wonderful',
                'edit_exciting',
            ),
        )

    def __repr__(self):
        """
        Wrapper for self.BulbDevice.__repr__()
        """

        return self._super().__repr__()

    def ping(self):
        """
        Ping port 6668 on the Bulb
        """

        return utils.ping(self.host, self.port)

    def _super(self):
        """
        Returns self.BulbDevice (shorthand)
        """

        return self.BulbDevice
