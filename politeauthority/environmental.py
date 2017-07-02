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
        '/data/logs/politeauthority/logs')


def get_temp_dir():
    return os.environ.get(
        'PA_BASE_TEMP_DIR',
        '/tmp/politeauthority/tmp')


def get_cache_dir():
    return os.environ.get(
        'PA_BASE_TEMP_DIR',
        '/tmp/politeauthority/cache')


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
        'port': os.environ.get('PA_MYSQL_PORT', 3306)
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

###############################################
#              STOCKY CRAP                    #
###############################################


def pa_stock_config():
    return os.environ.get(
        'PA_STOCKS_CONFIG',
        '/home/alix/repos/politeauthority/stocks/flask/config/config_dev.py')

# End File: politeauthority/politeauthority/environmental.py
