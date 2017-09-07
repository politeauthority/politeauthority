"""Misc
"""

from datetime import datetime


def markets_open(check_time=None):
    """
    Determines if markets are currently open, or open by defined by the date supplied.

    :return: The markets are open or not.
    :rtype: bool
    """

    if check_time:
        the_time = check_time
    else:
        the_time = datetime.now()
    import pdb
    pdb.set_trace()
    if the_time.hour + 2 > 9:
        return False
    if the_time.hour > 14:
        return False
    if the_time.strftime('%A') in ['Saturday', 'Sunday']:
        return False
    return True
