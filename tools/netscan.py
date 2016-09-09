#!/usr/bin/env python

import os
import sys
import xmltodict
from datetime import datetime
from politeauthority.scan import Scan
from politeauthority.driver_mysql import DriverMysql

database = {
    'user': 'root',
    'pass': 'cleancut',
    'host': 'localhost',
    'dbname': 'phinder'
}
db = DriverMysql(database)


def get_devices():
    d = {}
    known_devices = db.ex('select * from `phinder`.`devices`;')
    for kd in known_devices:
        d[kd[0]] = {
            'id': kd[0],
            'name': kd[1],
            'mac': kd[2],
            'last_seen': kd[3],
            'last_ip': kd[4],
            'person_id': kd[6]
        }
    return d


def save_new_device(device):
    vals = {
        # 'name': device['name'],
        'mac': device['mac'],
        'last_seen': device['scan_time'],
        'last_ip': device['current_ip'],
        'last_hostname': '',
    }
    qry = """INSERT INTO `phinder`.`devices`
        (mac,last_seen,last_ip,last_hostname)
        VALUES("%(mac)s","%(last_seen)s","%(last_ip)s","%(last_hostname)s");"""
    qry = qry % vals
    db.ex(qry)
    qry2 = """SELECT max(id) FROM `phinder`.`devices`;"""
    return db.ex(qry2)[0][0]


def update_device(device):
    qry = """UPDATE `phinder`.`devices` SET last_seen="%s", last_ip="%s"
        WHERE `mac`="%s";""" % (device['scan_time'], device['current_ip'], device['mac'])
    db.ex(qry)


def save_wittness(device_id, time_seen):
    qry = """INSERT INTO `phinder`.`witness` (device_id,date) VALUES(%s,"%s");""" % (device_id, time_seen)
    db.ex(qry)


def parse_scan_time(string_):
    return datetime.strptime(string_, '%a %b  %d %H:%M:%S %Y')


def parse_nmap(xml_phile):
    print '  Parsing %s' % xml_phile
    scan_string = open(xml_phile)
    netscan = dict(xmltodict.parse(scan_string))
    network_devices = {}
    scan_time = parse_scan_time(netscan['nmaprun']['runstats']['finished']['@timestr'])
    if 'host' not in netscan['nmaprun']:
        return network_devices
    for host in netscan['nmaprun']['host']:
        if host['status']['@state'] == 'up':
            ip = host['address'][0]['@addr']
            mac = host['address'][1]['@addr']
            network_devices[mac] = {
                'name': '',
                'mac': mac,
                'current_ip': ip,
                'scan_time': scan_time
            }
    return network_devices


def store_data(network_devices):
    known_devices = get_devices()
    print 'Found %s Devices of %s known' % (len(network_devices), len(known_devices))
    for mac, info in network_devices.iteritems():
        scanned_device_id = False
        for d_id, device in known_devices.iteritems():
            if device['mac'] == mac:
                scanned_device_id = d_id
        if not scanned_device_id:
            scanned_device_id = save_new_device(info)
            print 'Found new device %s' % mac
        else:
            update_device(info)

        if scanned_device_id in known_devices:
            if known_devices[scanned_device_id]['name']:
                print 'We found Device: %s' % known_devices[scanned_device_id]['name']
            # print known_devices[scanned_device_id]
        save_wittness(scanned_device_id, info['scan_time'])


if __name__ == '__main__':
    if os.geteuid() != 0:
        exit("""You need to have root privileges to run this script.\n
        Please try again, this time using 'sudo'. Exiting.""")
    scans = sys.argv[1]
    if ',' in scans:
        scans = scans.split(',')
    else:
        scans = [scans]
    print 'Running scan'
    network_devices = {}
    for scan in scans:
        scan_file = Scan().hosts(scan)
        network_devices = dict(network_devices, **parse_nmap(scan_file))
    print 'Proccessing scan output'
    store_data(network_devices)

# End File: politeauthority/tools/netscan.py
