#!/usr/bin/env python
"""
    Raspi
    some tools for working with the raspberry
"""

import os
import subprocess
import socket
import requests


class Raspi(object):

    def get_current_ssid(self, interface):
        connected_ssid = subprocess.check_output('iwgetid')
        if connected_ssid.strip() != '':
            ssid_name = connected_ssid[connected_ssid.find('ESSID:"') + 6:].replace('"', '').strip()
        else:
            ssid_name = False
        return ssid_name

    def get_local(self):
        gw = os.popen("ip -4 route show default").read().split()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((gw[2], 0))
        ipaddr = s.getsockname()[0]
        gateway = gw[2]
        return (ipaddr, gateway)

    def get_wan(self):
        return requests.get('https://ipapi.co/ip/').text

# EndFile: politeauthority/raspi.py
