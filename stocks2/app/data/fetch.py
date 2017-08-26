"""Fetch

Usage:
    fetch.py [options]

Options:
    --test
    --debug             Run the debugger.

"""
from docopt import docopt
import sys
import os
import requests
from datetime import datetime
import csv
import time
# from sqlalchemy.exc import importIntegrityError

from politeauthority import common

sys.path.append("../..")
from app import app
from app.models.company import Company
from app.models.quote import Quote

download_path = app.config.get('APP_DATA_PATH', '/data/politeauthority/')


def get_company_data_from_nasdaq():
    philes = __download_nasdaq_public_data()
    __process_nasdaq_public_data_market(philes['nasdaq'], 'nasdaq')
    __process_nasdaq_public_data_market(philes['nyse'], 'nyse')


def __download_nasdaq_public_data():
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


def __process_nasdaq_public_data_market(phile, market):
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


def get_quotes_from_google():
    base_url = "https://www.google.com/finance/historical?output=csv&q=%s"

    if not os.path.exists(download_path):
        os.makedirs(download_path)
    symbols = ['AAPL', 'TSLA', 'ERIC']
    companies = Company.query.filter(Company.symbol.in_(symbols)).all()
    companies_to_run = len(companies)
    count = 0
    for company in companies:
        count += 1
        app.logger.info("<%s> %s" % (company.symbol, company.name))
        app.logger.info("\tWorking %s/%s" % (count, companies_to_run))
        r = requests.get(base_url % company.symbol)
        if r.status_code != 200:
            app.logger.error('Bad Response: %s' % r.status_code)

        csv_file = os.path.join(download_path, "%s.csv" % company.symbol)
        app.logger.info('Downloading %s' % csv_file)
        reader = list(csv.DictReader(open(csv_file)))
        c = 0
        app.logger.info('Saving Quotes')
        total_rows = len(reader) - 1
        for row in reader:
            c += 1
            if c == 1:
                continue
            print row
            raw_date = datetime.strptime(row['\xef\xbb\xbfDate'], '%d-%b-%y')
            raw_open = row['Open']
            raw_high = row['High']
            raw_low = row['Low']
            raw_close = row['Close']
            if len(row) > 5:
                raw_volume = row['Volume']
            else:
                raw_volume = None
            q = Quote()
            q.company_id = company.id
            q.date = raw_date
            if raw_open not in ['-']:
                q.open = raw_open
            if raw_high not in ['-']:
                q.high = raw_high
            if raw_low not in ['-']:
                q.low = raw_low
            q.close = raw_close
            q.volume = raw_volume
            q.save()
            # try:
            #     q.save()
            # except Exception:
            #     print 'Record already exitst'
            if (c / 2) % 2:
                app.logger.info('%s\tProcessed: %s/%s' % (company, c, total_rows))
        company.save()
        time.sleep(2)


def test():
    print 'hi'
    print Company.query.filter(Company.symbol == 'AAPL').all()

if __name__ == "__main__":
    args = docopt(__doc__)
    # get_company_data_from_nasdaq()
    if args['--test']:
        print test
        test()
        exit()
    get_quotes_from_google()

# End File:
