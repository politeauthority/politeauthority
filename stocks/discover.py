from modules import discovery
from modules import company_collections



if __name__ == '__main__':
    companies = company_collections.disc_new_companies()
    for company in companies:
        print company.symbol
        print '\t%s' % info['comp'].name
        print '\tLast Sale:   %s' % company.price
        print '\t52 Week High: %s' % company.high_52_weeks
        print '\t52 Week Low:  %s' % company.low_52_weeks
        print '\n'

# End File:
