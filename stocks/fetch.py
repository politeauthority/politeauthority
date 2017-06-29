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
    --one_year            Backfill 1 year quote data from Google where we dont have
    --get_wiki            Get company wikipedia urls where we dont have them
    --daily               Runs after market close routines
    --update              Run daily update
    -d --debug            Run the console at debug level

    markets open between 7:30am - 2pm MTN
"""

from docopt import docopt
import os
import requests
from datetime import datetime
import csv
import wikipedia

from politeauthority import common
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from modules.quote import Quote
from modules.stocky import Stocky
from modules import company_collections
from modules import quote_collections
from one_fetch import base_companies_nyse_nasdaq

INTERSTING_SYMBOLS = ['YHOO', 'VSLR', 'YEXT', 'VERI', 'PSDO', 'SGH', 'APPN', 'AYX', 'SNAP', 'GDI', 'CLDR', 'OKTA',
                      'MULE']

current_dir = os.path.dirname(os.path.realpath(__file__))
download_path = os.path.join(environmental.get_temp_dir(), 'stocks')
db = DriverMysql(environmental.mysql_conf())

if environmental.build() == 'dev':
    LIMIT = 10
else:
    LIMIT = 7800


def get_one_year():
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    companies = company_collections.wo_meta('daily_google', limit=LIMIT)
    companies = company_collections.wo_meta(
        'daily_google',
        'datetime',
        '<=',
        datetime.now().replace(hour=14, minute=0, second=0),
        LIMIT)
    count = 0
    for company in companies:
        company.load()
        count += 1
        print "Working %s/%s" % (count, LIMIT)
        print "<%s> %s" % (company.symbol, company.name)
        url = "https://www.google.com/finance/historical?output=csv&q=%s" % company.symbol
        r = requests.get(url)
        if r.status_code != 200:
            if 'daily_google_fail' in company.meta:
                meta_fail = company.meta['daily_google_fail']
                meta_fail['value'] = meta_fail['value'] + 1
            else:
                meta_fail['meta_type'] = 'int'
                meta_fail['value'] = 1
            print 'Company Failed'
            company.save_meta(meta_fail)
            company.save()
            continue

        csv_file = os.path.join(download_path, "%s.csv" % company.symbol)
        year_file = csv_file
        print 'Downloading: %s' % csv_file
        with open(year_file, 'wb') as code:
            code.write(r.content)
        f = open(year_file, 'rb')
        reader = csv.reader(f)
        c = 0
        print 'Proccessing %s' % company.name
        total_quotes_before = len(quote_collections.get_by_company_id(company.id))
        for row in reader:
            c += 1
            if c == 1:
                continue
            raw_date = datetime.strptime(row[0], '%d-%b-%y')
            raw_open = row[1]
            raw_high = row[2]
            raw_low = row[3]
            raw_close = row[4]
            if len(row) > 5:
                raw_volume = row[5]
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
        meta = {
            'meta_key': 'one_year_google',
            'entity_id': company.id,
            'meta_type': 'datetime',
            'value': q.date
        }
        company.save_meta(meta)
        company.save()
        print c
        print 'Saved %s Quotes, Before we had %s\n' % (c, total_quotes_before)


def get_company_wikipedia_url():
    companies = company_collections.get_companies_needing_wikipedia_url(500)
    # companies = db.ex(qry)

    for c in companies:
        # g_search = "%s wikipedia" % c.name
        print c
        c.load()
        if 'wikipedia_url_fail' in c.meta:
            print 'found a already failed'
            meta_fail = c.meta['wikipedia_url_fail']
            meta_fail['value'] = meta_fail['value'] + 1
            c.save_meta(meta_fail)
            c.save()
            continue

        print c.name
        c.save()
        query_term = c.name
        query_term = query_term.replace('Inc.', '')
        query_term = common.remove_punctuation(query_term)
        query_term = query_term.strip()
        print query_term
        meta_wiki_search_e = {
            'meta_key': 'wiki_search_error',
            'entity_id': c.id,
            'meta_type': 'text',
        }
        try:
            wiki = wikipedia.page(query_term)
        except wikipedia.exceptions.PageError, e:
            meta_wiki_search_e['value'] = e
            c.save_meta(meta_wiki_search_e)
            print 'Could not Find wiki artical for %s, Error: %s' % (c.name, e)
            print ''
            continue
        except wikipedia.exceptions.DisambiguationError, e:
            meta_wiki_search_e['value'] = e
            c.save_meta(meta_wiki_search_e)
            print e
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
            'meta_type': 'pickle',
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
                'meta_type': 'varchar',
                'value': wiki.url
            }
            print 'saving wikipedia_url'
            c.save_meta(meta_wikipedia_url)
        else:
            meta_wikipedia_url_fail = {
                'meta_key': 'wikipedia_url_fail',
                'entity_id': c.id,
                'meta_type': 'int',
                'value': 1
            }
            c.save_meta(meta_wikipedia_url_fail)
        print ''


def show_company_wikipedia_url():
    companies = company_collections.by_meta('wikipedia_url', 1)
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


def daily():
    print 'Daily'
    # get all companies needing daily
    companies = company_collections.wo_meta(
        'daily_process',
        'datetime',
        '<=',
        datetime.now().replace(hour=14, minute=0, second=0),
        LIMIT)
    total_companies = len(companies)
    count = 0
    errors = 0
    for c in companies:
        count += 1
        print '%s of %s %s' % (count, total_companies, c)
        try:
            share = Stocky().process(c)
        except Exception, e:
            errors += 1
            print '\tError(%s): %s' % (errors, e)
            if errors == 5:
                print 'Hit 5 API Errors, quitting'
                exit()
        print '\t%s' % share.get_price()

        print ''


def daily_updates():
    print 'Daily Updates'
    companies = company_collections.wo_meta(
        'daily_process',
        'datetime',
        '<=',
        datetime.now().replace(hour=14, minute=0, second=0),
        LIMIT)
    for company in companies:
        company.load()
        qry = """
            SELECT distinct(left(`quote_date`, 10)) d, count(*) c
            FROM `stocks`.`quotes`
            WHERE
                `company_id` = %s

            GROUP BY 1;""" % company.id
        print qry
        quotes = db.ex(qry)
        quote_dates = []
        for q in quotes:
            quote_date = datetime.strptime(q[0], '%Y-%m-%d')
            tt = quote_date.timetuple()
            quote_dates.append(tt.tm_yday)
            print quote_date
            print "%s : %s" % (q[0], q[1])
        quote_dates = sorted(quote_dates)
        print quote_dates
        print company.name
        print company.ts_update
        print company.meta
        print ''


if __name__ == '__main__':
    args = docopt(__doc__)
    if args['--build_from_nasdaq']:
        base_companies_nyse_nasdaq.run()
    if args['--daily']:
        daily()
    if args['--update']:
        daily_updates()
    if args['--one_year']:
        get_one_year()
    if args['--get_wiki']:
        get_company_wikipedia_url()
