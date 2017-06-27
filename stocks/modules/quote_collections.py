from datetime import datetime
from datetime import timedelta

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from company import Company

db = DriverMysql(environmental.mysql_conf())


def get_by_company_id(company_id):
    limit = 40
    qry = """
        SELECT *
        FROM `stocks`.`quotes`
        WHERE `company_id` = %s
        ORDER BY `quote_date` DESC
        LIMIT 365;
        """ % company_id
    res = db.ex(qry)
    return res


# def get_by_company_id(company_id):
#     qry = """
#         SELECT max(`high`), `date`, id
#         FROM stocks.quotes
#         WHERE `company_id` = %s;""" % company_id
#     print qry
#     return db.ex(qry)

# End File:
