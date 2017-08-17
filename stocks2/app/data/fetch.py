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
from datetime import datetime
import csv

from politeauthority import common

sys.path.append("../..")
from app import app
from app.models.company import Company

download_path = app.config.get('APP_DATA_PATH', '/data/politeauthority/')


def build_nasdaq_data():
    philes = download_nasdaq_public_data()
    process_nasdaq_public_data_market(philes['nasdaq'], 'nasdaq')
    process_nasdaq_public_data_market(philes['nyse'], 'nyse')


def download_nasdaq_public_data():
    """
    Grabs base company data to kick off the database. This should only need to be run once really.

    """
    nasdaq_dir = os.path.join(download_path, 'tmp', 'nasdaq_data')
    if not os.path.exists(nasdaq_dir):
        os.makedirs(nasdaq_dir)
    url_nasdaq = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    url_nyse = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"

    downloaded_files = {}

    app.logger.info('Downloading Nasdaq')
    file_nasdaq = os.path.join(nasdaq_dir, 'nasdaq_%s.csv' % common.file_safe_date(datetime.now()))
    r = requests.get(url_nasdaq)
    with open(os.path.join(download_path, file_nasdaq), 'wb') as code:
        code.write(r.content)
    downloaded_files['nasdaq'] = file_nasdaq

    app.logger.info('Downloading NYSE')
    file_nyse = os.path.join(nasdaq_dir, 'nasdaq_%s.csv' % common.file_safe_date(datetime.now()))
    r = requests.get(url_nyse)
    with open(os.path.join(download_path, file_nyse), 'wb') as code:
        code.write(r.content)
    downloaded_files['nyse'] = file_nyse
    return downloaded_files


def process_nasdaq_public_data_market(phile, market):
    f = open(phile, 'rb')
    reader = csv.reader(f)
    count = 0
    for row in reader:
        count += 1
        if count == 1:
            continue
        vals = {
            'symbol': row[0],
            'name': row[1],
            'last_sale': row[2],
            'market_cap': row[3],
            'ipo_year': row[5],
            'sector': row[6],
            'industry': row[7],
            'exchange': market,
        }
        c = Company.query.filter(
            Company.symbol == vals['symbol'], Company.exchange == market).all()
        if c:
            app.logger.info('Already Have Data for %s' % c[0].name)
            continue
        c = Company()
        c.symbol = vals['symbol']
        c.name = vals['name']
        if vals['last_sale'] != "n/a":
            c.price = vals['last_sale']
        else:
            c.price = 0
        c.market_cap = vals['market_cap']
        c.ipo_year = vals['ipo_year']
        c.sector = vals['sector']
        c.industry = vals['industry']
        c.exchange = vals['exchange']
        print c.price
        c.save()
        app.logger.info('Saved: %s' % c.name)

if __name__ == "__main__":
    args = docopt(__doc__)
    build_nasdaq_data()

# End File:
