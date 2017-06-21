"""
fetch.py

Usage:
    fetch.py [--get_daily] [options]
    fetch.py  (-h | --help)

Options:
    -h --help             Shows this screen.
    --get_interesting     Fetch Interesting companies only.
    --build_from_nasdaq   Populates company table and last_price column,
                             most likely from the day. Best to run this EOB
    --one_year             Backfill 1 year quote data from Google
    --daily               Runs after market close routines
    -d --debug            Run the console at debug level

    markets open between 7:30am - 2pm MTN
"""

from docopt import docopt
import os
import requests
from datetime import datetime
from datetime import timedelta
import csv
from yahoo_finance import Share
# from google import google
import wikipedia

from politeauthority import common
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from modules.company import Company
from modules.quote import Quote
from modules import company_collections

from one_fetch import base_companies_nyse_nasdaq

INTERSTING_SYMBOLS = ['YHOO', 'VSLR', 'YEXT', 'VERI', 'PSDO', 'SGH', 'APPN', 'AYX', 'SNAP', 'GDI', 'CLDR', 'OKTA',
                      'MULE']

current_dir = os.path.dirname(os.path.realpath(__file__))
download_path = os.path.join(current_dir, 'downloads')
db = DriverMysql(environmental.mysql_conf())


def get_one_year():
    companies = company_collections.get_companies_wo_meta('one_year', 500)
    for company in companies:
        print "<%s> %s" % (company.symbol, company.name)
        # print company
        url = "https://www.google.com/finance/historical?output=csv&q=%s" % company.symbol
        r = requests.get(url)
        year_file = os.path.join(download_path, "%s.csv" % company.symbol)
        with open(year_file, 'wb') as code:
            code.write(r.content)
        f = open(year_file, 'rb')
        reader = csv.reader(f)
        c = 0
        for row in reader:
            c += 1
            if c == 1:
                continue
            q = Quote()
            q.company_id = company.id
            q.date = datetime.strptime(row[0], '%d-%b-%y')
            if row[1] not in ['-']:
                q.open = row[1]
            if row[2] not in ['-']:
                q.high = row[2]
            if row[3] not in ['-']:
                q.low = row[3]
            q.close = row[4]
            q.volume = row[5]
            q.save()
        meta_wiki_search = {
            'meta_key': 'one_year',
            'entity_id': company.id,
            'type': 'datetime',
            'value': q.date
        }
        company.save_meta(meta_wiki_search)
        print 'Saved %s Quotes\n' % c


def update_data_from_yahoo(only_interesting=False):
    if only_interesting:
        where_qry = '`symbol` IN ("%s")' % '","'.join(INTERSTING_SYMBOLS)
    else:
        where_qry = """`run_company` = 1 AND `last_update_ts` <= "%s"  """ % (datetime.now() - timedelta(hours=20))
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
        except Exception, e:
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


def get_company_wikipedia_url():
    companies = company_collections.get_companies_for_wiki_seach(100)
    # companies = db.ex(qry)

    for c in companies:
        # g_search = "%s wikipedia" % c.name
        if 'wikipedia_url_fail' in c.meta:
            print c.meta
            print 'found a already failed'
            c.save()
            continue

        print c.name
        c.save()
        query_term = c.name
        query_term = query_term.replace('Inc.', '')
        query_term = common.remove_punctuation(query_term)
        query_term = query_term.strip()
        print query_term
        try:
            wiki = wikipedia.page(query_term)
        except wikipedia.exceptions.PageError, e:
            print 'Could not Find wiki artical for %s, Error: %s' % (c.name, e)
            print ''
            continue
        wiki_url = common.remove_punctuation(wiki.url[30:]).replace('_', ' ')

        wsd = {  # wiki search data
            'sim_title': common.similar(c.name, wiki.title),
            'sim_url': common.similar(c.name, wiki_url),
            'wiki_url': wiki.url,
            'wiki_url_text': common.remove_punctuation(wiki.url[30:])
        }
        wsd['sim_total'] = wsd['sim_title'] + wsd['sim_url']
        if wsd['sim_total'] >= 1:
            print 'its good'
            wsd['sim_accepted'] = True
        else:
            print 'not right'
            wsd['sim_accepted'] = False

        print "wiki title:   %s" % wiki.title
        print "wiki url:     %s" % wiki.url
        print "Wiki URL sim: %s" % wsd['wiki_url_text']
        print "sim title:    %s" % wsd['sim_title']
        print "sim url:      %s" % wsd['sim_url']
        print 'sim total:    %s' % wsd['sim_total']

        meta_wiki_search = {
            'meta_key': 'wiki_search',
            'entity_id': c.id,
            'type': 'pickle',
            'value': wsd
        }
        c.save_meta(meta_wiki_search)
        # print wiki.content
        # search_results = google.search(g_search, 1)
        # wiki_url = None
        # if len(search_results) > 0:
        #     for s in search_results:
        #         print s.link
        #         if 'en.wikipedia.org' in s.link:
        #             wiki_url = s.link
        #             continue

        if wsd['sim_accepted']:
            meta_wikipedia_url = {
                'meta_key': 'wikipedia_url',
                'entity_id': c.id,
                'type': 'varchar',
                'value': wiki.url
            }
            print 'saving wikipedia_url'
            c.save_meta(meta_wikipedia_url)
        else:
            meta_wikipedia_url_fail = {
                'meta_key': 'wikipedia_url_fail',
                'entity_id': c.id,
                'type': 'int',
                'value': 1
            }
            c.save_meta(meta_wikipedia_url_fail)
        print ''


def show_company_wikipedia_url():
    companies = company_collections.get_companies_by_meta('wikipedia_url', 1)
    # companies = db.ex(qry)
    if len(companies) == 0:
        print 'No companies found with wikipedia_url'
    for c in companies:
        print c.id
        print c.name
        c.load_meta()
        # print c.meta
        if 'wikipedia_url' in c.meta:
            print c.meta['wikipedia_url']['value']
    # print all_companies

if __name__ == '__main__':
    args = docopt(__doc__)
    if args['--build_from_nasdaq']:
        base_companies_nyse_nasdaq.run()
    if args['--daily']:
        update_data_from_yahoo()
    if args['--one_year']:
        get_one_year()
    if args['--get_interesting']:
        update_data_from_yahoo(only_interesting=True)
