"""
ENVIRONMENTAL VARS
"""
import os


###############################################
#              OUTPUT LOCATIONS               #
###############################################
def get_logging_dir():
    return os.environ.get(
        'PA_BASE_LOGGING_DIR',
        '/data/logs/politeauthority')


def get_temp_dir():
    return os.environ.get(
        'PA_BASE_LOGGING_DIR',
        '/tmp/politeauthority')

# End File: politeauthority/politeauthority/environmental.py
