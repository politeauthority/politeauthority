"""
    Load porfolio
"""
import os
import csv
from datetime import datetime


def load_portfolio_from_csv():
    portfolio_file = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        '../portfolio.csv'
    )
    with open(portfolio_file, 'rb') as csvfile:
        spamreader = csv.DictReader(csvfile, delimiter=',')
        stocks = {}
        for row in spamreader:
            sym = row['Symbol']
            if row['Symbol'] not in stocks:
                if not row['Sale Count']:
                    row['Sale Count'] = 0
                if not row['Sale Date']:
                    row['Sale Date'] = None
                else:
                    row['Sale Date'] = datetime.strptime(row['Sale Date'], '%m-%d-%Y')
                stocks[sym] = {}
                stocks[sym]['symbol'] = row['Symbol']
                stocks[sym]['purchases'] = []
                stocks[sym]['sells'] = []
                stocks[sym]['active_shares'] = 0
            stocks[sym]['purchases'].append({
                'price': float(row['Purchase Price']),
                'count': int(row['Purchase Count']),
                'date':  datetime.strptime(row['Purchase Date'], '%m-%d-%Y')
                })
            stocks[sym]['sells'].append({
                'price': row['Sale Price'],
                'count': row['Sale Count'],
                'date':  row['Sale Date']
                })
    for sym, stock in stocks.iteritems():
        for p in stock['purchases']:
            stocks[sym]['active_shares'] += p['count']
        for s in stock['sells']:
            if s['count']:
                stocks[sym]['active_shares'] = stocks[sym]['active_shares'] - int(s['count'])
    return stocks
