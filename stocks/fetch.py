"""
fetch.py

Usage:
  fetch.py [--get_daily] [options]
  fetch.py  (-h | --help)

Options:
  -h --help             Shows this screen.
  --get_interesting      Fetch Interesting companies only.
  --build_from_nasdaq   Populates company table and last_price column,
                            most likely from the day. Best to run this EOB
  -d --debug            Run the console at debug level



  markets open between 7:30am - 2pm MTN
);

"""

from docopt import docopt
import os
import urllib2
import requests
from datetime import datetime
# from datetime import timedelta
import csv
from yahoo_finance import Share


from politeauthority import common
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from modules.company import Company
from modules.quote import Quote


current_dir = os.path.dirname(os.path.realpath(__file__))
download_path = os.path.join(current_dir, 'downloads')
db = DriverMysql(environmental.mysql_conf())


def download_data():
    """
        Mostly grabs just base data to start the DB
    """
    url_nasdaq = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download"
    url_nyse = "http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NYSE&render=download"

    if not os.path.exists(download_path):
        os.mkdir(download_path)

    downloaded_files = {}

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


def process_data(philes):
    process_data_market(philes['nasdaq'], 'nasdaq')
    process_data_market(philes['nyse'], 'nyse')


def process_data_market(phile, market):
    f = open(phile, 'rb')
    reader = csv.reader(f)
    c = 0
    for row in reader:
        c += 1
        if c == 1:
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
            'last_update_ts': datetime.now()
        }
        if vals['last_sale'] in ['n/a']:
            continue
        qry = """SELECT * FROM `stocks`.`companies`
                 WHERE `exchange`="%s" AND `name`="%s" """ % (market, row[1])
        print qry
        company = db.ex(qry)
        if len(company) == 0:
            qry = """INSERT INTO `stocks`.`companies`
                     (`symbol`, `name`, `last_sale`, `market_cap`, `ipo_year`, `sector`, `industry`,
                      `exchange`, `last_update_ts`)
                     VALUES
                     ("%(symbol)s", "%(name)s", "%(last_sale)s", "%(market_cap)s",
                      "%(ipo_year)s", "%(sector)s", "%(industry)s", "%(exchange)s", "%(last_update_ts)s" )"""
            print qry % vals
            db.ex(qry % vals)
        else:
            print "Already have: %s " % vals['name']
    os.rm(phile)


def update_data_from_yahoo(only_interesting=False):
    INTERSTING_SYMBOLS = ['YHOO', 'VSLR']
    if only_interesting:
        where_qry = '`symbol` IN ("%s")' % '","'.join(INTERSTING_SYMBOLS)
    else:
        where_qry = "`run_company` = 1"
    qry = """SELECT `id`
             FROM `stocks`.`companies`
             WHERE
             %s
             ORDER BY last_update_ts;""" % where_qry
    print qry
    companies = db.ex(qry)
    total_companies = len(companies)
    debug = True
    print total_companies
    print ' '
    count = 0
    for c in companies:
        count += 1
        print '%s of %s' % (count, total_companies)
        company = Company()
        company.get_company_by_id(c[0])
        print company.name

        try:
            share = Share(company.symbol)
        except urllib2.HTTPError, e:
            print e
            print "Couldn't Fetch Data for %s" % c[2]
            continue
        company.last_sale = share.get_price()
        company.high_52_weeks = share.data_set['YearHigh']
        company.low_52_weeks = share.data_set['YearLow']
        company.high_day = share.get_days_high()
        company.low_day = share.get_days_low()
        company.save()
        quote = Quote()
        quote.company_id = company.id
        quote.day_high = company.high_day
        quote.day_low = company.low_day
        quote.current = company.last_sale
        quote.date = datetime.now()
        quote.save()
        if debug:
            print company.name
            print company.id
            print "current_price  %s" % company.last_sale
            print "high_52_weeks  %s" % company.high_52_weeks
            print "low_52_weeks   %s" % company.low_52_weeks
            print "high_day  %s" % company.high_day
            print "low_day   %s" % company.low_day


        print ''
        print ''
        print ''

        # c_update = {
        #     'company_id': c[0],
        #     'symbol': company.symbol,
        #     'exchange': company.exchange,
        #     'last_sale': company.current_price,
        #     'high_52_weeks': company.high_52_weeks,
        #     'low_52_weeks': company.low_52_weeks,
        #     'high_day': high_day,
        #     'low_day': low_day
        # }
        # __update_company(c_update)


def __update_company(info):
    if info['symbol'] in [None]:
        return False
    if info['exchange'] in [None]:
        return False
    write_fields = []
    if info['last_sale'] not in [None]:
        write_fields.append('last_sale')
    if info['high_52_weeks'] not in [None]:
        write_fields.append('last_sale')
    if info['low_52_weeks'] not in [None]:
        write_fields.append('last_sale')
    info['last_update_ts'] = datetime.now()
    write_fields.append('last_update_ts')
    set_sql = ''
    for f in write_fields:
        set_sql += """`%s`="%s", """ % (f, info[f])
    set_sql = set_sql[:-2]
    sql = """UPDATE `stocks`.`companies`
             SET
             %s
             WHERE
                `exchange`="%s"
                AND
                `symbol`="%s"; """ % (
        set_sql,
        info['exchange'],
        info['symbol']
    )
    db.ex(sql)
    print 'updated'
    print sql
    day_fields = []
    if 'high_day' in info and info['high_day']:
        day_fields.append('high_day')
    if 'low_day' in info and info['low_day']:
        day_fields.append('low_day')
    if 'low_day' and 'high_day' in day_fields:
        qry = """INSERT INTO `stocks`.`quotes`
                 (`company_id`, `symbol`, `day_high`, `day_low`, `date`)
                 VALUES ("%s", "%s", "%s", "%s", "%s");""" % (
            info['company_id'],
            info['symbol'],
            info['high_day'],
            info['low_day'],
            datetime.now()
        )
        print qry
        db.ex(qry)
    print ''


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['--build_from_nasdaq']:
        philes = download_data()
        process_data(philes)
        print philes
    if args['--get_daily']:
        update_data_from_yahoo()
    if args['--get_interesting']:
        update_data_from_yahoo(only_interesting=True)
