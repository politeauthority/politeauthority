"""
    Company Model

    COMPANY TABLE
    CREATE TABLE `companies` (
      `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `symbol` varchar(10) DEFAULT NULL,
      `name` varchar(255) DEFAULT NULL,
      `last_sale` decimal(12,2) DEFAULT NULL,
      `market_cap` decimal(20,2) DEFAULT NULL,
      `ipo_year` varchar(10) DEFAULT NULL,
      `sector` varchar(255) DEFAULT NULL,
      `industry` varchar(255) DEFAULT NULL,
      `exchange` varchar(50) DEFAULT NULL,
      `last_update_ts` datetime DEFAULT NULL,
      `high_52_weeks` decimal(20,2) DEFAULT NULL,
      `low_52_weeks` decimal(20,2) DEFAULT NULL,
      `run_company` tinyint(1) DEFAULT NULL,
      PRIMARY KEY (`id`)
    );


"""
from datetime import datetime

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

from meta import Meta

db = DriverMysql(environmental.mysql_conf())


class Company(object):

    def __init__(self):
        self.id = None
        self.symbol = None
        self.name = None
        self.last_sale = None
        self.market_cap = None
        self.ipo_year = None
        self.sector = None
        self.industry = None
        self.exchange = None
        self.last_update = None
        self.high_52_weeks = None
        self.low_52_weeks = None
        self.run_company = None

    def get_company_by_id(self, company_id):
        self.id = company_id
        qry = """SELECT *
                 FROM `stocks`.`companies`
                 WHERE
                    `id` = %s;
              """ % self.id
        company_row = db.ex(qry)
        if len(company_row) <= 0:
            return None
        self.build_from_row(company_row[0])
        self.load_meta()

    def build_from_row(self, company_row):
        self.id = company_row[0]
        self.symbol = company_row[1]
        self.name = company_row[2]
        self.last_sale = company_row[3]
        self.market_cap = company_row[4]
        self.ipo_year = company_row[5]
        self.sector = company_row[6]
        self.industry = company_row[7]
        self.exchange = company_row[8]
        self.last_update = company_row[9]
        self.high_52_weeks = company_row[10]
        self.low_52_weeks = company_row[11]
        self.run_company = company_row[12]

    def save(self, save_none_vals=[]):
        if not self.id:
            print 'Cant save the object not enough info'
            return False
        set_sql = ''
        if self.symbol:
            set_sql += """`%s`='%s', """ % ("symbol", self.symbol)
        if self.name:
            set_sql += """`%s`='%s', """ % ("name", self.name)
        if self.last_sale:
            set_sql += """`%s`='%s', """ % ("last_sale", self.last_sale)
        if self.market_cap:
            set_sql += """`%s`='%s', """ % ("market_cap", self.market_cap)
        if self.ipo_year:
            set_sql += """`%s`='%s', """ % ("ipo_year", self.ipo_year)
        if self.sector:
            set_sql += """`%s`='%s', """ % ("sector", self.sector)
        if self.industry:
            set_sql += """`%s`='%s', """ % ("industry", self.industry)
        if self.exchange:
            set_sql += """`%s`='%s', """ % ("exchange", self.exchange)
        if self.high_52_weeks:
            set_sql += """`%s`='%s', """ % ("high_52_weeks", self.high_52_weeks)
        if self.low_52_weeks:
            set_sql += """`%s`='%s', """ % ("low_52_weeks", self.low_52_weeks)
        if self.run_company:
            set_sql += """`%s`='%s', """ % ("run_company", self.run_company)

        if not set_sql:
            return False
        if set_sql:
            set_sql += '`last_update_ts`="%s", ' % datetime.now()
            set_sql = set_sql[:-2]

        sql = """UPDATE `stocks`.`companies`
                 SET
                 %s
                 WHERE
                    `id`=%s; """ % (
            set_sql,
            self.id
        )
        db.ex(sql)
        return True

    def load_meta(self):
        m = Meta()
        m.schema = 'stocks'
        info = {}
        info['entity_id'] = self.id
        info['entity_type'] = 'company'
        self.meta = m.load_meta(info)

    def save_meta(self, meta_info):
        m = Meta()
        m.schema = 'stocks'
        meta_info['entity_id'] = self.id
        meta_info['entity_type'] = 'company'
        m.save(meta_info)
