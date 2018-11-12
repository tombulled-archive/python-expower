"""
Contains:
    int_to_hex()
"""

def int_to_hex(integer, size=2):
    """
    Convert {integer} to string hex of size {size}

    :param(int) integer - Integer to be 'hexified'
    :param(int) size - Size of the hexified string

    Example usage:
        >>> int_to_hex(1)
        >>> '01'
        >>> int_to_hex(23)
        >>> '17'
    """

    return hex(integer)[2:].zfill(size)
