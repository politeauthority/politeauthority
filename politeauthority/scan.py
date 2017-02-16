#!/usr/bin/env python
"""
    NetScan
"""

import os
import subprocess
from datetime import datetime
import xmltodict
from politeauthority import environmental


class NetScan(object):

    def hosts(self, ip_range):
        self.output_file = os.path.join(
            self.__save_dir(),
            str(datetime.now()).replace(' ', '-') + '.xml'
        )
        cmd = 'nmap -sP -oX %s %s' % (
            self.output_file,
            ip_range)
        subprocess.check_output(
            cmd,
            shell=True)
        return self.output_file

    def __save_dir(self):
        the_dir = os.path.join(
            environmental.get_temp_dir(),
            'netscan'
        )
        if not os.path.exists(the_dir):
            os.makedirs(the_dir)
        return the_dir

    def parse_nmap(self, xml_phile):
        """
            Parses a nmap file into a dict
            @params
                xml_phile: nmap xml file location
        """
        print '  Parsing %s' % xml_phile
        scan_string = open(xml_phile)
        netscan = dict(xmltodict.parse(scan_string))
        network_devices = {}
        scan_time = self.__parse_scan_time(netscan['nmaprun']['runstats']['finished']['@timestr'])
        if 'host' not in netscan['nmaprun']:
            return network_devices
        for host in netscan['nmaprun']['host']:
            if host['status']['@state'] == 'up':
                if 'address' in host and len(host['address']) > 0:
                    print host['address']
                    ip = host['address'][0]['@addr']
                    mac = host['address'][1]['@addr']
                    network_devices[mac] = {
                        'name': '',
                        'mac': mac,
                        'current_ip': ip,
                        'scan_time': scan_time
                    }
        return network_devices

    def __parse_scan_time(self, string_):
        return datetime.strptime(string_, '%a %b  %d %H:%M:%S %Y')

# EndFile: politeauthority/scan.py
