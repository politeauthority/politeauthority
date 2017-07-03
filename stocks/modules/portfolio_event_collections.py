from decimal import Decimal
from politeauthority import common
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from portfolio_event import PortfolioEvent
from company import Company

db = DriverMysql(environmental.mysql_conf())


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
        companies[company.id] = company
    portfolio = {
        'events': events,
    }
    if not load_full:
        return portfolio
    totals = {
        'amt_invested': 0,
        'cash_in': Decimal(229.32),
        'amt_total_value': 0,
        'amt_standing': 0,
        'percent_val': 0
    }
    for e in events:
        e.company = companies[e.company_id]
        if e.type == 'buy':
            totals['amt_invested'] += (e.price * e.count)
            totals['amt_total_value'] += (e.company.price * e.count)
    totals['cash_available'] = totals['cash_in'] - totals['amt_invested']
    totals['amt_standing'] = totals['amt_invested'] - totals['amt_total_value']
    totals['percent_val'] = common.get_percentage(
        totals['amt_standing'],
        totals['amt_invested'])
    portfolio = {
        'companies': companies,
        'events': events,
        'totals': totals
    }
    return portfolio
