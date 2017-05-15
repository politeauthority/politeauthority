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
from yahoo_finance import Share
from datetime import datetime
from portfolio import stocks
from politeauthority import common


def format_curreny(number):
    str_num = str(number)
    if len(str(str_num)[str(str_num).find('.')+1:]) < 2:
        return str_num + '0'
    else:
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

# End File: politeauthority/stocks/stock.py
