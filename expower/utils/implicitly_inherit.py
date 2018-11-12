"""
Contains:
    implicitly_inherit()
"""

def implicitly_inherit(src, dst, attrs=(), overwrite=True):
    """
    Implicitly inheir {attrs} from {src} to {dst}

    :param(object) src - Object containing {attrs}
    :param(object) dst - Object to inherit {attrs}
    :param(bool) overwrite - Whether to overwrite {dst}'s
        ... attrs if they already contain a value
    """

    for attr in attrs:
        if not hasattr(src, attr):
            continue

        if hasattr(dst, attr) and not overwrite:
            continue

        setattr(dst, attr, getattr(src, attr))
