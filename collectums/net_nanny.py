import sys

from politeauthority.mosquitto import Mosquitto
from politeauthority.netscan import NetScan
from politeauthority import environmental
config = {}
config['host'] = 'chatsec.org'


def main(ip_scan_range):
    netscan = NetScan()
    hosts_file = netscan.hosts(ip_scan_range)
    hosts = netscan.parse_nmap(hosts_file)
    for mac, host in hosts.iteritems():
        Mosquitto(config).publish(
            'net_nanny/%s' % environmental.get_machine_id(),
            host)


if __name__ == "__main__":
    main(sys.argv[1])
