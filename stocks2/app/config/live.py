from politeauthority import environmental

mysql_conf = environmental.mysql_conf()
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (
    mysql_conf['user'],
    mysql_conf['pass'],
    mysql_conf['host'],
    3306,
    'stocks2')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = False
TESTING = False
THREADS_PER_PAGE = 2
# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"
PA_APP_DATA_PATH = '/data/'
