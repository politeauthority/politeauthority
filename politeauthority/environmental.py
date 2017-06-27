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
        'PA_BASE_TEMP_DIR',
        '/tmp/politeauthority')


def get_machine_id():
    return os.environ.get(
        'PA_MACHINE_ID',
        'UNKNOWN')

###############################################
#              MySQL CRAP                   #
###############################################


def mysql_conf():
    return {
        'host': os.environ.get('PA_MYSQL_HOST', None),
        'user': os.environ.get('PA_MYSQL_USER', None),
        'pass': os.environ.get('PA_MYSQL_PASS', None),
    }

###############################################
#              BUILD                          #
###############################################


def build():
    return os.environ.get(
        'PA_BUILD',
        'dev')

###############################################
#              TWITTER CRAP                   #
###############################################


def twitter_consumer_key():
    return os.environ.get(
        'PA_TWITTER_CONSUMER_KEY',
        None)


def twitter_consumer_secret():
    return os.environ.get(
        'PA_TWITTER_CONSUMER_SECRET',
        None)


def twitter_access_key():
    return os.environ.get(
        'PA_TWITTER_ACCESS_KEY',
        None)


def twitter_access_secret():
    return os.environ.get(
        'PA_TWITTER_ACCESS_SECRET',
        None)


def slack_url():
    return os.environ.get(
        'PA_SLACK_URL',
        None)


# End File: politeauthority/politeauthority/environmental.py
