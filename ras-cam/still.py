#!/usr/bin/env python

import subprocess
from datetime import datetime
print datetime.now()
file_name = '/home/pi/photos/temp_%s.jpg' % str(datetime.now())[:19].replace(' ', 'T').replace(':', '_')
cmd = ['raspistill',
       '-rot 270',
       '-o',
       file_name,
       '']
print ' '.join(cmd)
subprocess.check_output(
        ' '.join(cmd),
        shell=True)
try:
    cmd = "scp %s alix@chatsec.org:~/photos" % file_name
    subprocess.check_output(cmd, shell=True)
except Exception, e:
    print e

