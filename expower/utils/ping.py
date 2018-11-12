from .. import constants
import socket

"""
Imports:
    ..constants
    socket

Contains:
    ping()
"""

def ping(host, port=constants.PORT):
    """
    Ping {port} on {host} to check it's open

    :param(str) host - Host IP address
    :param(int) port - Host Port, defaults to 6668

    :returns(bool) - Whether {port} is open on {host}
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    return sock.connect_ex((host, port)) == 0
