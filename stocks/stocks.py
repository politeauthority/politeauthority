"""
    Stocks.py

    example stock sample
        vslr = {
        'symbol': 'VSLR',
        'purchases': [{
            'price': 2.80,
            'shares': 2,
            'date': datetime(2017, 4, 19),
        }]
}
"""
import csv
from yahoo_finance import Share
from datetime import datetime
import urllib2

from politeauthority import common
from politeauthority import color


def format_curreny(number, color_it=True):
    if number < 0:
        co = 'red'
    else:
        co = 'green'
    str_num = str(round(number, 2))
    if len(str(str_num)[str(str_num).find('.')+1:]) < 2:
        _str = str_num + '0'
    else:
        _str = str_num
    if color_it:
        return color.fore(co, "$" + _str)
    else:
        return "$" + _str


def format_percentage(number):
    if number < 0:
        co = 'red'
    else:
        co = 'green'
    return color.fore(co, str(number) + "%")


def load_portfolio_from_csv():
    with open('portfolio.csv', 'rb') as csvfile:
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


if __name__ == '__main__':
    stocks = load_portfolio_from_csv()
    total_investment = 0
    total_portfolio = 0
    total_delta = 0
    for symbol, info in stocks.iteritems():
        if info['active_shares'] < 1:
            continue
        days_in_stock = 0
        try:
            share = Share(info['symbol'])
        except urllib2.HTTPError, e:
            print e
            continue
        current_price = float(share.get_price())
        price_delta = 0
        cash_in_stock = 0
        value_in_stock = 0
        for p in info['purchases']:
            total_int = round((current_price - p['price']) * p['count'], 2)
            price_delta += total_int
            cash_in_stock += p['price'] * p['count']
            value_in_stock += current_price * p['count']
            total_investment += cash_in_stock
            total_portfolio += current_price * p['count']
            days_in_stock += (datetime.now() - p['date']).days
        total_string = format_curreny(price_delta)
        if days_in_stock == 0:
            days_in_stock = 1
        print '%(symbol)s\t(%(active_shares)s) %(price_from_purchase)s' % {
            'symbol': info['symbol'],
            'price_from_purchase': total_string,
            'active_shares': info['active_shares']
        }
        stock_delta_percent = common.get_percentage(value_in_stock - cash_in_stock, value_in_stock)
        print '\tDays in\t %s' % days_in_stock
        print '\tCash in Stock\t %s' % cash_in_stock
        print '\tValue in Stock\t %s' % value_in_stock
        print stock_delta_percent
        print ''
    if total_portfolio <= total_investment:
        tp_s = color.fore('red', format_curreny(total_portfolio, False))
    else:
        tp_s = color.fore('green', format_curreny(total_portfolio, False))
    print "Portfolio:"
    print "\tinvested: %s" % format_curreny(total_investment, False)
    print "\t%s \t(%s)\t(%s)" % (
        tp_s,
        format_percentage(common.get_percentage(price_delta, total_investment)),
        format_curreny(price_delta)
        )
        return str_num

total_investment = 0
total_portfolio = 0
total_winloss = 0
for s in stocks:
    share = Share(s['symbol'])
    current_price = float(share.get_price())
    total_portfolio += current_price * len(s['purchases'])
    total = 0
    days_in_avg = 0
    percentage_avg = 0
    for p in s['purchases']:
        purchase_price_diff = round((current_price - p['price']) * p['shares'], 2)
        purchase_percent_diff = common.get_percentage(purchase_price_diff, p['price'] * p['shares'])
        total += purchase_price_diff
        total_investment += p['price'] * p['shares']
        total_winloss += float(total)
        # print str(total)[str(total).find('.')+1:]
        # print ''
        # print '(%s - %s) * %s' % (current_price, s['purchase'], s['shares'])
        # print total * s['shares']
        # print s['purchase']
        days_in_avg += (datetime.now() - p['date']).days
        percentage_avg += purchase_percent_diff

    print '%(symbol)s\t$%(price_from_purchase)s' % {
        'symbol': s['symbol'],
        'price_from_purchase': total
    }
    days_in_avg = float(days_in_avg) / len(s['purchases'])
    if days_in_avg == 0:
        days_in_avg = 1
    percentage_avg = float(percentage_avg) / len(s['purchases'])
    speed = days_in_avg / percentage_avg
    print '\t%s  %s' % (days_in_avg, percentage_avg)
    print '\t%s' % speed
    print ''

print "Portfolio total value: $%s  %s" % (total_investment, total_portfolio)
print """Deltas:
    $%s
    %s%%""" % (
    format_curreny(total_winloss),
    common.get_percentage(total_winloss, total_investment)
)
>>>>>>> dda98a6eff63ce117647dce1f440cbe36de88626

# End File: politeauthority/stocks/stock.py
