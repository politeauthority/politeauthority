"""Fetch

Usage:
    fetch.py [options]

Options:
    --debug             Run the debugger.

"""
from docopt import docopt
import sys
import os
import requests

sys.path.append("../..")
import app
from app.models.company import Company


def download_nasdaq_public_data():
    """
    Grabs base company data to kick off the database. This should only need to be run once really.
    """
    url_nasdaq = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    url_nyse = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"
    import pdb
    pdb.set_trace()
    if not os.path.exists(app.config['DOWNLOAD_PATH']):
        os.mkdir(download_path)

    downloaded_files = {}

    print download_path
    print 'Downloading Nasdaq'
    file_nasdaq = os.path.join(download_path, 'nasdaq_%s.csv' % common.file_safe_date(datetime.now()))
    r = requests.get(url_nasdaq)
    with open(os.path.join(download_path, file_nasdaq), 'wb') as code:
        code.write(r.content)
    downloaded_files['nasdaq'] = file_nasdaq

    print 'Downloading NYSE'
    file_nyse = os.path.join(download_path, 'nasdaq_%s.csv' % common.file_safe_date(datetime.now()))
    r = requests.get(url_nyse)
    with open(os.path.join(download_path, file_nyse), 'wb') as code:
        code.write(r.content)
    downloaded_files['nyse'] = file_nyse
    return downloaded_files


if __name__ == "__main__":
    args = docopt(__doc__)
    print args
    c = Company()
    c.symbol = 'TEST'
    c.name = 'Test Company'
    c.price = 50.08
    c.save()

    print c

    import pdb
    pdb.set_trace()

# End File: 
