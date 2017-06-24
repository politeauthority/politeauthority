from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from company import Company

db = DriverMysql(environmental.mysql_conf())


def by_meta(meta_key, limit=10):
    qry = """
          SELECT c.`id`
          FROM `stocks`.`companies` c
            JOIN `stocks`.`meta` m
                ON c.id = m.entity_id AND m.entity_type="company"
          WHERE
            `meta_key`="%s"; """ % meta_key
    if limit:
        qry += 'LIMIT %s' % limit

    return __qry_to_companies(qry)


def wo_meta(meta, limit=10):
    qry = """
             SELECT c.id
             FROM `stocks`.`companies` c
             LEFT JOIN (SELECT *
                        FROM `stocks`.`meta` m
                        WHERE 
                            m.`meta_key` != "%(meta_key)s" AND
                            m.`entity_type` = "company"
                        LIMIT 1) x
                ON c.`id` = x.`entity_id`
            WHERE x.`entity_id` is NULL
            ORDER BY c.`ts_update` ASC
            LIMIT %(limit)s;
          """ % {
        'meta_key': meta,
        'limit': limit}
    print qry
    return __qry_to_companies(qry)


def get_companies_daily(limit):
    qry = """
        SELECT c.`id`
        FROM `stocks`.`companies` c
        JOIN `stocks`.`meta` m
            ON
            c.id = m.entity_id AND
            m.entity_type="company"
        WHERE
            `meta_key`="daily" AND
            val_date >= '%s'"""
    if limit:
        qry += 'LIMIT %s' % limit
    return __qry_to_companies(qry)


def __qry_to_companies(qry):
    res = db.ex(qry)
    companies = []
    for c_id in res:
        com = Company()
        com.get_company_by_id(c_id)
        companies.append(com)
    return companies
