"""
CREATE TABLE `companies` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `symbol` varchar(10) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `last_sale` decimal(12,2) DEFAULT NULL,
  `market_cap` decimal(20,2) DEFAULT NULL,
  `ipo_year` varchar(10) DEFAULT NULL,
  `sector` varchar(255) DEFAULT NULL,
  `industry` varchar(255) DEFAULT NULL,
  `exchange` varchar(50) DEFAULT NULL,
  `last_update_ts` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)

);

"""

import os
import requests
from datetime import datetime
import csv
from politeauthority.driver_mysql import DriverMysql

from politeauthority import common
from politeauthority import environmental

current_dir = os.path.dirname(os.path.realpath(__file__))
download_path = os.path.join(current_dir, 'downloads')
db = DriverMysql(environmental.mysql_conf())


def download_data():
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
        # print row
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
        # exit()

if __name__ == '__main__':
    philes = download_data()
    process_data(philes)
    print philes

