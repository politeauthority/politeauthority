from datetime import datetime
from datetime import timedelta

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from company import Company

db = DriverMysql(environmental.mysql_conf())


def get_count():
    qry = """SELECT count(*) as c FROM `stocks`.`companies`;"""
    return db.ex(qry)


def get_recently_modified(page=1):
    limit = 40
    qry = """
        SELECT `id`
        FROM `stocks`.`companies`
        ORDER BY `ts_updated` DESC LIMIT %s OFFSET %s;
        """ % (limit, (limit * page) - limit)
    return __qry_to_companies(qry, False)


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

    return __qry_to_companies(qry, False)


def wo_meta(meta, meta_type=None, comparison=None, value=None, limit=10):
    or_val_sql = ''
    if meta_type and comparison and value:
        or_val_sql = """OR (`val_%s` %s "%s") """ % (meta_type, comparison, value)
    qry = """
        SELECT c.id
        FROM `stocks`.`companies` c
            LEFT JOIN `stocks`.`meta` m
                ON
                    c.`id` = m.`entity_id` AND
                    m.`meta_key` = "%(meta_key)s"
        WHERE
            m.`meta_key` is NULL
            %(or_val_sql)s
        ORDER BY c.`ts_updated` ASC
        LIMIT %(limit)s;
    """ % {
        'meta_key': meta,
        'or_val_sql': or_val_sql,
        'limit': limit
    }
    print qry
    return __qry_to_companies(qry, False)


def get_companies_needing_wikipedia_url(limit=10):
    qry = """
        SELECT c.id as id, mm.val_int
        FROM `stocks`.`companies` c
            LEFT JOIN `stocks`.`meta` m
                ON
                    c.`id` = m.`entity_id` AND
                    m.`meta_key` = "wikipedia_url"
            LEFT JOIN `stocks`.`meta` mm
                ON
                    c.`id` = m.`entity_id` AND
                    mm.`meta_key` = "wikipedia_url_fail"

        WHERE
            m.`meta_key` is NULL AND
            (
                mm.`val_int` is NULL OR
                mm.`val_int` < 4
            )
        ORDER BY c.`ts_updated` ASC
        LIMIT %(limit)s;
    """ % {
        'limit': limit
    }
    print qry
    return __qry_to_companies(qry, False)


def get_companies_daily(limit, load_full=False):
    mtn_market_close = datetime.now().replace(hour=14, minute=0, second=0)
    print mtn_market_close
    qry = """
        SELECT c.`id`
            FROM `stocks`.`companies` c
            JOIN `stocks`.`meta` m
                ON
                c.id = m.entity_id AND
                m.entity_type="company"
        WHERE
            `meta_key`="daily" AND
            `val_datetime` <= '%s'""" % str(mtn_market_close)
    if limit:
        qry += ' LIMIT %s' % limit
    print qry
    return __qry_to_companies(qry, load_full)


def disc_new_companies():
    qry = """
        SELECT c.id
            FROM `stocks`.`companies` c
            -- JOIN `stocks`.`meta` m
            --     ON
            --         c.id = m.entity_id AND
            --         c.entity_type = 'company' AND
            --         m`meta_key` = 'daily'
            WHERE
                ipo_year IN ("2017", "2016")

            ORDER BY price ASC;"""
    return __qry_to_companies(qry)


def __qry_to_companies(qry, load_full):
    res = db.ex(qry)
    companies = []
    for co in res:
        com = Company()
        com.get_company_by_id(co[0], load_full)
        companies.append(com)
    return companies
