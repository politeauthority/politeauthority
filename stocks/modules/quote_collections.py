from datetime import datetime
from datetime import timedelta

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from quote import Quote

db = DriverMysql(environmental.mysql_conf())


def get_by_company_id(company_id, date_back=None):
    if not date_back:
        date_back = datetime.now() + timedelta(days=365)
    limit = 365
    qry = """
        SELECT *
        FROM `stocks`.`quotes`
        WHERE `company_id` = %s
        ORDER BY `quote_date` DESC
        LIMIT %s;
        """ % (company_id, limit)
    res = db.ex(qry)
    qs = []
    for r in res:
        qs.append(Quote().build_from_row(r))
    return qs


def get_by_company_ids(company_ids, date_back=None):
    if not date_back:
        date_back = datetime.now() + timedelta(days=365)
    company_sql = ''
    for c in company_ids:
        company_sql += '%s,' % c
    company_sql = company_sql[:-1]

    qry = """
        SELECT *
        FROM `stocks`.`quotes`
        WHERE
            `company_id` IN(%s) AND
            `quote_date` >= "%s"
        ORDER BY `quote_date` DESC;
        """ % (company_sql, date_back)
    res = db.ex(qry)
    qs = []
    for r in res:
        qs.append(Quote().build_from_row(r))

    ret_keyed = {}
    return_set = []
    for q in qs:
        date_key = q.date.strftime('%Y-%m-%d')
        print date_key
        if q.date not in ret_keyed:
            ret_keyed[date_key] = q.close
        else:
            ret_keyed[date_key] += q.close
    for x, y in ret_keyed.iteritems():
        q = Quote()
        q.date = x
        q.close = y
        return_set.append(q)

    return qs

# def get_by_company_id(company_id):
#     qry = """
#         SELECT max(`high`), `date`, id
#         FROM stocks.quotes
#         WHERE `company_id` = %s;""" % company_id
#     print qry
#     return db.ex(qry)

# End File:
