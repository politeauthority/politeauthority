import timeago

from politeauthority.driver_mysql import DriverMysql
from politeauthority import environmental


db = DriverMysql(environmental.mysql_conf())


def monitor_devices(devices):
    qry = """SELECT * FROM `phinder`.`devices` where id IN (%s);""" % devices
    devices = db.ex(qry)

    for d in devices:
        print 'Device: %s' % d[1]
        print '\tLast seen %s' % timeago.format(d[3])
        print '\tSeen by %s' % d[7]


def monitor_people(peoples):
    return None

if __name__ == '__main__':
    monitor_devices("69, 70")
    monitor_people(1)

# End File monitor.py
