from politeauthority import common
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

import quote_collections
from portfolio_event import PortfolioEvent
from company import Company

db = DriverMysql(environmental.mysql_conf())

current_cash_in = float(350.00)


def get_by_portfolio_id(portfolio_id, load_full=False):
    qry = """
        SELECT *
        FROM `stocks`.`portfolio_events`
        WHERE
            `portfolio_id` = %s;
    """ % portfolio_id
    rows = db.ex(qry)
    if len(rows) <= 0:
        return None
    events = []
    company_ids = []
    for row in rows:
        pe = PortfolioEvent().build_from_row(row)
        events.append(pe)
        if pe.company_id not in company_ids:
            company_ids.append(pe.company_id)
    companies = {}
    for c in company_ids:
        company = Company().get_company_by_id(c)
        company.stake = 0
        company.value = 0
        companies[company.id] = company
    portfolio = {
        'events': events,
    }
    if not load_full:
        return portfolio
    totals = {
        'amt_invested': 0,
        'cash_in': current_cash_in,
        'amt_total_value': 0,
        'amt_standing': 0,
        'percent_val': 0
    }
    company_ids = set()
    for e in events:
        e.company = companies[e.company_id]
        company_ids.add(e.company_id)
        if e.type == 'buy':
            totals['amt_invested'] += (e.price * e.count)
            totals['amt_total_value'] += (e.company.price * e.count)
            e.company.stake += (e.price * e.count)
            e.company.value += (e.company.price * e.count)
    totals['cash_available'] = float(totals['cash_in']) - float(totals['amt_invested'])
    totals['amt_standing'] = totals['amt_invested'] - totals['amt_total_value']
    totals['percent_val'] = common.get_percentage(
        totals['amt_standing'],
        totals['amt_invested'])
    quotes = quote_collections.get_by_company_ids(company_ids)
    print quotes
    portfolio = {
        'companies': companies,
        'events': events,
        'totals': totals
    }
    return portfolio
