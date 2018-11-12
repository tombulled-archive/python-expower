import pprint

"""
Imports:
    pprint

Contains:
    <BaseSchema>
"""

class BaseSchema(tuple):
    """
    Class to allow searching of device schema
    """

    def __repr__(self):
        """
        Returns a string representation of the object
        ... in the form:
            (
                {
                    {key_1}: val_1,
                    ...
                },
                ...
            )

        Uses: pprint.pformat
        """

        data = '(\n'

        for item in self:
            data += ' '

            data += '\n '.join(pprint.pformat(item).splitlines())

            data += ',\n'

        data += '\n)'

        return data

    def get(self, **kwargs):
        """
        Return a schema entry which matches **kwargs

        E.g:
            schema.get(code='led_switch')
        """

        for entry in self:
            for kwarg, val in kwargs.items():
                if entry.get(kwarg, None) != val:
                    break
            else:
                return entry
