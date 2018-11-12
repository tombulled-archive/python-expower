from . import schema_keys
from . import scenes
from . import state_keys

"""
Imports:
    .schema_keys
    .scenes
    .state_keys
"""

# E.g convert 'scene_1' to 'soft'
SCENE_TO_NAME = \
{
    schema_keys.SCENE_1: scenes.SOFT,
    schema_keys.SCENE_2: scenes.COLOURFUL,
    schema_keys.SCENE_3: scenes.EXCITING,
    schema_keys.SCENE_4: scenes.WONDERFUL,
}

# E.g convert 'scene_1' to 1
SCENE_TO_INDEX = \
{
    scenes.LEISURE: 0,
    scenes.SOFT: 1,
    scenes.COLOURFUL: 2,
    scenes.EXCITING: 3,
    scenes.WONDERFUL: 4,
}

# E.g convert 'led_switch' to index 0
SCHEMA_KEY_TO_DPS_INDEX = \
{
    schema_keys.LED_SWITCH: 0,
    schema_keys.WORK_MODE: 1,
    schema_keys.BRIGHT_VALUE: 2,
    schema_keys.TEMP_VALUE: 3,
    schema_keys.COLOUR_DATA: 4,
    schema_keys.SCENE_DATA: 5,
    schema_keys.FLASH_SCENE_1: 6,
    schema_keys.FLASH_SCENE_2: 7,
    schema_keys.FLASH_SCENE_3: 8,
    schema_keys.FLASH_SCENE_4: 9,
}

# E.g. convert 'flash_scene_1' to 'scene_1'
FLASH_SCENE_TO_SCENE = \
{
    schema_keys.FLASH_SCENE_1: schema_keys.SCENE_1,
    schema_keys.FLASH_SCENE_2: schema_keys.SCENE_2,
    schema_keys.FLASH_SCENE_3: schema_keys.SCENE_3,
    schema_keys.FLASH_SCENE_4: schema_keys.SCENE_4,
}

# E.g. convert 'on' to 'led_switch'
STATE_KEY_TO_SCHEMA_KEY = \
{
    state_keys.ON: schema_keys.LED_SWITCH,
    state_keys.MODE: schema_keys.WORK_MODE,
    state_keys.BRIGHTNESS: schema_keys.BRIGHT_VALUE,
    state_keys.TEMPERATURE: schema_keys.TEMP_VALUE,
    state_keys.COLOUR: schema_keys.COLOUR_DATA,
    state_keys.SCENE: schema_keys.SCENE_DATA,
    state_keys.SCENES: schema_keys.FLASH_SCENES,
}
