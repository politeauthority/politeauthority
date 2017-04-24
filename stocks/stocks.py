from datetime import datetime
from yahoo_finance import Share
from portfolio import stocks


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
    # print s['purchase']
    # print current_price
    total = format_curreny(round((current_price - s['purchase']) * s['shares'], 2))
    total_investment += s['purchase'] * s['shares']
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

print total_investment
print format_curreny(total_winloss)
# End File: politeauthority/stocks/stock.py
