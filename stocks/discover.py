from modules import discovery


if __name__ == '__main__':
    tech = discovery.emerging_tech_stocks()
    for symbol, info in tech.iteritems():
        print symbol
        print '\t%s' % info['comp'].name
        print '\tLast Sale:   %s' % info['comp'].last_sale
        print '\t52 Week High: %s' % info['comp'].high_52_weeks
        print '\t52 Week Low:  %s' % info['comp'].low_52_weeks
        print '\n'

# End File:
