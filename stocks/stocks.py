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
from portfolio import stocks
from politeauthority import common


def format_curreny(number):
    str_num = str(number)
    if len(str(str_num)[str(str_num).find('.')+1:]) < 2:
        return str_num + '0'
    else:
        return str_num

total_investment = 0
total_winloss = 0
for s in stocks:
    share = Share(s['symbol'])
    current_price = float(share.get_price())
    total = 0
    for p in s['purchases']:
        total_int = round((current_price - p['price']) * p['shares'], 2)
        total += total_int
        total_investment += p['price'] * p['shares']
        total_winloss += float(total)
        # print str(total)[str(total).find('.')+1:]
        # print ''
        # print '(%s - %s) * %s' % (current_price, s['purchase'], s['shares'])
        # print total * s['shares']
        # print s['purchase']
    print '%(symbol)s\t%(price_from_purchase)s' % {
        'symbol': s['symbol'],
        'price_from_purchase': total
    }
    print ''

print "Portfolio total value: $%s" % total_investment
print """Deltas:
    $%s
    %s%%""" % (
    format_curreny(total_winloss),
    common.get_percentage(total_winloss, total_investment)
)

# End File: politeauthority/stocks/stock.py
