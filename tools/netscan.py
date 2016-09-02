#!/usr/bin/env python

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
        }
    return d


def save_new_device(device):
    vals = {
        'name': device['name'],
        'mac': device['mac'],
        'last_seen': device['scan_time'],
        'last_ip': device['current_ip'],
        'last_hostname': '',
        'people_id': '',
    }
    qry = """INSERT INTO `phinder`.`devices`
        (name,mac,last_seen,last_ip,last_hostname,people_id)
        VALUES("%(name)s","%(mac)s","%(last_seen)s","%(last_ip)s","%(last_hostname)s","%(people_id)s");"""
    qry = qry % vals
    db.ex(qry)
    qry2 = """SELECT max(id) FROM `phinder`.`devices`;"""
    return db.ex(qry2)[0][0]


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
    print known_devices
    print 'Found %s Devices' % len(network_devices)
    for mac, info in network_devices.iteritems():
        print mac
        scanned_device_id = False
        for d_id, device in known_devices.iteritems():
            if device['mac'] == mac:
                scanned_device_id = d_id
        if not scanned_device_id:
            scanned_device_id = save_new_device(info)
        save_wittness(scanned_device_id, info['scan_time'])
    print known_devices

# def __store_witness()

if __name__ == '__main__':
    scans = sys.argv[1]
    if ',' in scans:
        scans = scans.split(',')
    else:
        scans = [scans]
    print 'Running scan'
    network_devices = {}
    print 'Proccessing scan output'
    for scan in scans:
        scan_file = Scan().hosts(scan)
        network_devices = dict(network_devices, **parse_nmap(scan_file))
    store_data(network_devices)
# End File: politeauthority/tools/netscan.py
