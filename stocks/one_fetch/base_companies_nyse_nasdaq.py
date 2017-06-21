"""
    Download data for Nasdaq and Nyse companies. to build base companies table data.
"""
import sys
import os
import requests
import csv
from datetime import datetime

from politeauthority import common
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from modules.company import Company

download_path = os.path.join(environmental.get_temp_dir(), 'stocks')
db = DriverMysql(environmental.mysql_conf())


def download_nasdaq_public_data():
    """
        Mostly grabs just base data to start the DB
    """
    url_nasdaq = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    url_nyse = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"

    if not os.path.exists(download_path):
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


def process_nasdaq_public_data(philes):
    process_nasdaq_public_data_market(philes['nasdaq'], 'nasdaq')
    process_nasdaq_public_data_market(philes['nyse'], 'nyse')


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
        qry = """SELECT * FROM `stocks`.`companies`
                 WHERE `exchange`="%s" AND `name`="%s" """ % (market, row[1])
        company = db.ex(qry)
        if len(company) == 0:
            c = Company()
            c.symbol = vals['symbol']
            c.name = vals['name']
            c.price = vals['last_sale']
            c.market_cap = vals['market_cap']
            c.ipo_year = vals['ipo_year']
            c.sector = vals['sector']
            c.industry = vals['industry']
            c.exchange = vals['exchange']
            c.save()
            print 'Saved %s' % c
        else:
            print "Already have: %s " % vals['name']
    # os.rm(phile)


def run():
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    philes = download_nasdaq_public_data()
    process_nasdaq_public_data(philes)
    print 'complete!'
