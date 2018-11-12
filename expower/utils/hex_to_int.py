"""
Contains:
    hex_to_int()
"""

def hex_to_int(hex_str):
    """
    Convert {hex_str} to an integer

    :param(str) hex_str - Hex string (No 0x)

    :returns(int) - Integer value of {hex_str}

    Example:
        >>> hex_to_int('5')
        >>> 5
        >>> hex_to_int('20')
        >>> 32
    """

    return int(hex_str, 16)
