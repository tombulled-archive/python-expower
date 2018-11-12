from ... import constants

"""
Imports:
    ..constants
"""

def on_connection_reset \
        (
            val = None,
            retry = constants.networking.MAX_CONNECTION_ATTEMPTS,
        ):
    """
    Decorator-Wrapper to assign {val} in case {retry} attempts fail to
    ... establish a connection

    :param val - Gets returned if connection fails too many times
    :param retry - Try this many times to connect before giving up

    :returns - Success: Output of decorated function
        ... Failure: {val}

    Pseudocode:
        Do {retry} times to:
            Try:
                Connect and call function
            Except the connection gets reset:
                keep trying
        # If got here, failed too many times
        return {val}

    Level: on_connection_reset
    """

    def decorator(func):
        """
        Nested Decorator for on_connection_reset

        :param func - Function to decorate

        :returns - {func} wrapped

        Level: on_connection_reset.decorator
        """

        def wrapper(*args, **kwargs):
            """
            Nested Wrapper for on_connection_reset

            :param *args - *args to be passed to {func}
            :param **kwargs - **kwargs to be passed to {func}

            :returns - Success: Output of decorated function
                ... Failure: {val}

            Level: on_connection_reset.decorator.wrapper
            """

            for _ in range(retry): # Try {retry} times
                try:
                    return func(*args, **kwargs) # Attempt to call the function
                except ConnectionResetError as error_connection_reset:
                    pass # Keep attempting

            return val # Failed too many times, return {val}

        return wrapper

    return decorator
