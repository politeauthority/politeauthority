#!/usr/bin/env python

import subprocess
from datetime import datetime

photo_name = 'temp_'
file_name = '/home/pi/photos/%s%s.jpg' % (
    photo_name,
    str(datetime.now())[:19].replace(' ', 'T').replace(':', '_')
    )
cmd = ['raspistill',
       '-rot 270',
       '-o',
       file_name]

print 'Taking picture'
subprocess.check_output(
        ' '.join(cmd),
        shell=True)
picture_uploaded = None
print 'Trying to send the picture'
try:
    cmd = "scp %s alix@chatsec.org:~/photos" % file_name
    subprocess.check_output(cmd, shell=True)
    picture_uploaded = True
    print 'Uploaded the picture'
except Exception, e:
    print 'Failed to send the picture'
    print e
    picture_uploaded = False

if picture_uploaded:
    subprocess.check_output('rm %s' % file_name)
    print 'Picture Removed'
