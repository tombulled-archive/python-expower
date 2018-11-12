from .. import BaseSchema

"""
Imports:
    ..BaseSchema

Contains:
    create_schema()
"""

def create_schema(schema):
    """
    Convert {schema} to an instance of <Schema>
    ... Where <Schema> inherits from <BaseSchema>

    :param(tuple) schema - Device schema

    :returns(object) - A <Schema> instance
    """

    class Schema(BaseSchema):
        """
        Disposable class to initialise <BaseSchema>
        """

        def __new__(self):
            """
            Calls super().__new__ with {schema}
            """

            return super().__new__(self, schema)

    return Schema()
