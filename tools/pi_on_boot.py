from politeauthority.raspi import Raspi
from politeauthority import environmental
from politeauthority import slacky

connected = Raspi().get_local()
ssid = Raspi().get_current_ssid('wlan0')
wan_ip = Raspi().get_wan()
message = "%s Reporting in. Connected to %s at IP:%s, Gateway:%s, WAN: %s" % (
    environmental.get_machine_id(),
    ssid,
    connected[0],
    connected[1],
    str(wan_ip))
print message
slacky.send(message)

# End File: politeauthority/tools/pi_on_boot.py
