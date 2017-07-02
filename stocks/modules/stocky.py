"""
    Stocky
    Wrapper for Yahoo Stock API

"""
from yahoo_finance import Share

from politeauthority import common
from quote import Quote


class Stocky(object):

    def process(self, company):
        """
        """
        company.load()
        try:
            share = Share(company.symbol)
        except Exception, e:
            print e
            print "ERROR: Couldn't Fetch Data for %s" % company.name
            self.__update_error(company)
            return False
        if 'LastTradeDateTimeUTC' not in share.data_set:
            print 'ERROR: No Trade Date'
            self.__update_error(company)
            return False
        dividend_stock = self.check_divided_stock(share)
        if dividend_stock:
            print 'Saved Dividend stock'
            company.save_meta(dividend_stock)
        q = Quote()
        q.company_id = company.id
        q.open = share.data_set['Open']
        q.close = share.get_price()
        q.high = share.get_days_high()
        q.low = share.get_days_low()
        q.volume = share.data_set['Volume']
        q.date = common.utc_to_mountain(share.data_set['LastTradeDateTimeUTC'])
        q.save()
        meta = {
            'meta_key': 'last_price',
            'entity_id': company.id,
            'meta_type': 'datetime',
            'value': q.date
        }
        company.price = share.get_price()
        company.save_meta(meta)
        company.save()
        return share

    def check_divided_stock(self, share):
        if 'DividendShare' in share.data_set:
            if 'DividendShare' not in share.data_set:
                div_m = {
                    'meta_key': 'dividend_stock',
                    'meta_type': 'pickle',
                    'value': {
                        'DividendShare': share.data_set['DividendShare'],
                        'DividendYield': share.data_set['DividendYield'],
                        'DividendPayDate': share.data_set['DividendPayDate'],
                        'ExDividendDate': share.data_set['ExDividendDate'],
                    },
                }
                return div_m
        return False

    def __update_error(self, company):
        m = {
            'meta_key': 'yahoo_error',
            'meta_type': 'int',
            'value': 1,
        }
        if 'yahoo_error' in company.meta:
            m['value'] += m['value'] + 1
        company.save_meta(m)

# End File:
