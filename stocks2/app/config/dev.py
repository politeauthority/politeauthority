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
THREADS_PER_PAGE = 2
DOWNLOAD_PATH = '/tmp/politeauthority/download'

