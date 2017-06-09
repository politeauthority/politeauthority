from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from company import Company

db = DriverMysql(environmental.mysql_conf())


def get_companies_by_meta(meta_key, limit=None, exists=True):
    if exists:
        qry = """SELECT c.`id`
                 FROM `stocks`.`companies` c
                 JOIN `stocks`.`meta` m
                    ON c.id = m.entity_id AND m.entity_type="company"
                 WHERE
                    `key`="%s" """ % meta_key
    else:
        qry = """SELECT c.`id`
                 FROM `stocks`.`companies` c
                 LEFT JOIN `stocks`.`meta` m
                    ON
                        c.id = m.entity_id
                        AND
                        m.entity_type="company"
                        AND
                        m.key="%s" """ % meta_key
    if limit:
        qry += 'LIMIT %s' % limit
    print qry
    res = db.ex(qry)
    companies = []
    for c_id in res:
        com = Company()
        com.get_company_by_id(c_id)
        companies.append(com)
    return companies
