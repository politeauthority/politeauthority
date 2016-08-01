#!/usr/bin/env python

import sys
from politeauthority.scan import Scan

if __name__ == '__main__':
    print Scan().hosts(sys.argv[1])

# End File: politeauthority/tools/netscan.py
