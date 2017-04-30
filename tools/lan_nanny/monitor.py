import timeago

from politeauthority.driver_mysql import DriverMysql
from politeauthority import environmental


db = DriverMysql(environmental.mysql_conf())


def monitor_devices(devices):
    qry = """SELECT * FROM `phinder`.`devices` where id = 70;"""
    devices = db.ex(qry)

    for d in devices:
        print 'Device: %s' % d[1]
        print '\t Last seen %s' % timeago.format(d[3])
        print d


if __name__ == '__main__':
    monitor_devices(70)
