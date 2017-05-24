import subprocess

from politeauthority.raspi import Raspi
from politeauthority import environmental

connected = Raspi().get_local()
ssid = Raspi().get_current_ssid('wlan0')
wan_ip = Raspi().get_wan()
print connected
print wan_ip
message = "%s Reporting in. Connected to %s at IP:%s, Gateway:%s, WAN: %s" % (
    environmental.get_machine_id(),
    ssid,
    connected[0],
    connected[1],
    str(wan_ip))
print message
exit()
cmd = """curl -X POST -H 'Content-type: application/json' --data '{"text":"%s"}' """
cmd += """https://hooks.slack.com/services/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"""
cmd = cmd % message
subprocess.call(cmd, shell=True)

# End File: politeauthority/tools/pi_on_boot.py
