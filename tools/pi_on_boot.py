import subprocess

from politeauthority.raspi import Raspi

connected = Raspi().get_local()
ssid = Raspi().get_current_ssid('wlan0')
wan_ip = Raspi().get_wan()
print connected

message = "Connected to %s at IP:%s, Gateway:%s, WAN: %s" % (ssid, connected[0], connected[1], wan_ip)
print message
cmd = """curl -X POST -H 'Content-type: application/json' --data '{"text":"%s"}' """
cmd += """https://hooks.slack.com/services/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"""
cmd = cmd % message
subprocess.call(cmd, shell=True)

# End File: politeauthority/tools/pi_on_boot.py
