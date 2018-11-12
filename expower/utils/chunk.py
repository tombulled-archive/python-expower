"""
Contains:
    chunk()
"""

def chunk(lst, size):
    """
    Yield successive n-sized chunks from l.

    Reference: https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """

    for index in range(0, len(lst), size):
        yield lst[index:index + size]
