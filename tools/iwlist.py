"""

"""
import operator


from politeauthority.netscan import NetScan


if __name__ == '__main__':
    current_nodes = NetScan().parse_iwlist('/home/pi/tmp_data/wlan0.txt')
    for mac, node in current_nodes.iteritems():
        print mac
        print node
    x = {1: 2, 3: 4, 4: 3, 2: 1, 0: 0}
    sorted_x = sorted(x.items(), key=operator.itemgetter(1))
    print x