"""Fetch

Usage:
    fetch.py [options]

Options:
    --debug             Run the debugger.

"""
from docopt import docopt
import sys

sys.path.append("../..")
import app
from app.models.company import Company

if __name__ == "__main__":
    args = docopt(__doc__)
    print args
    print app
    c = Company()
    c.symbol = 'TEST'
    c.name = 'Test Company'

    print c

