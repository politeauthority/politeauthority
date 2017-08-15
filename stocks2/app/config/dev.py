import os
from politeauthority import environmental

mysql_conf = environmental.mysql_conf()
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s:%s/%s' % (
    mysql_conf['user'],
    mysql_conf['pass'],
    mysql_conf['host'],
    3306,
    'stocks2')
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
TESTING = True
THREADS_PER_PAGE = 2
APP_DATA_PATH = os.environ.get('PA_APP_DATA_PATH', '/home/alix/pas_data/')

