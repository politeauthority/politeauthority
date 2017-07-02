import os
from politeauthority import environmental

# Statement for enabling the development environment
DEBUG = False

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
CACHE_DIR = environmental.get_cache_dir()
LOG_DIR = environmental.get_logging_dir()
WEB_IP = '0.0.0.0'
WEB_PORT = 5000

# Define the database - we are working with
mysql_conf = environmental.mysql_conf()
DB_USER = mysql_conf['host']
DB_PASS = mysql_conf['pass']
DB_HOST = mysql_conf['host']
DB_PORT = '3306'
DB_NAME = 'stocks'

SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (
    DB_USER,
    DB_PASS,
    DB_HOST,
    DB_PORT,
    DB_NAME)

DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
