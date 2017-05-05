"""

"""
import sys
import operator

from politeauthority.netscan import NetScan


if __name__ == '__main__':
    scan = NetScan()
    nodes = scan.run_iwlist('wlan0')
    sorty = sorted(nodes.items(), key=lambda nodes: nodes[1]['signal_strength'], reverse=True)
    for s in sorty:
        print s[1]['ESSID']
        print s[1]['signal_strength']
        print s[1]['signal_level']
        print ''

