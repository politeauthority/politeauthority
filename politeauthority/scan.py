#!/usr/bin/env python
"""
    Scan
"""

import os
import subprocess
from datetime import datetime
from politeauthority import environmental


class Scan(object):

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

# EndFile: politeauthority/scan.py
