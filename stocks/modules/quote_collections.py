from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql


db = DriverMysql(environmental.mysql_conf())


def get_by_company_id(company_id):
    limit = 365
    qry = """
        SELECT *
        FROM `stocks`.`quotes`
        WHERE `company_id` = %s
        ORDER BY `quote_date` DESC
        LIMIT %s;
        """ % (company_id, limit)
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
