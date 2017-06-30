"""
    Company Model

    COMPANY TABLE
    CREATE TABLE `stocks`.`companies` (
      `id`                  BIGINT(20) unsigned NOT NULL AUTO_INCREMENT,
      `symbol`              VARCHAR(10) DEFAULT NULL,
      `name`                VARCHAR(255) DEFAULT NULL,
      `price`               DECIMAL(20,4) DEFAULT NULL,
      `market_cap`          DECIMAL(20,4) DEFAULT NULL,
      `ipo_year`            VARCHAR(10) DEFAULT NULL,
      `sector`              VARCHAR(255) DEFAULT NULL,
      `industry`            VARCHAR(255) DEFAULT NULL,
      `exchange`            VARCHAR(50) DEFAULT NULL,
      `high_52_weeks`       DECIMAL(20,4) DEFAULT NULL,
      `high_52_weeks_date`  DATETIME DEFAULT NULL,
      `low_52_weeks`        DECIMAL(20,4) DEFAULT NULL,
      `low_52_weeks_date`   DATETIME DEFAULT NULL,
      `run_company`         TINYINT(1) DEFAULT NULL,
      `ts_created`          DATETIME DEFAULT CURRENT_TIMESTAMP,
      `ts_updated`          DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      KEY `symbol` (`symbol`),
      UNIQUE KEY `unique_index` (`symbol`, `exchange`)
    );

"""

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql
from politeauthority.meta import Meta

db = DriverMysql(environmental.mysql_conf())
company_table = 'stocks.companies'
m = Meta()
m.schema = 'stocks'


class Company(object):

    def __init__(self):
        self.id = None
        self.symbol = None
        self.name = None
        self.price = None
        self.market_cap = None
        self.ipo_year = None
        self.sector = None
        self.industry = None
        self.exchange = None
        self.last_update = None
        self.high_52_weeks = None
        self.high_52_weeks_date = None
        self.low_52_weeks = None
        self.low_52_weeks_date = None
        self.run_company = None
        self.ts_updated = None

        self.loaded = []

    def __repr__(self):
        return '<Company %r, %r>' % (self.symbol, self.name)

    def get_company_by_id(self, company_id, full=True):
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
        if full:
            self.load()
        return self

    def get_by_symbol(self, symbol, full=True):
        self.symbol = symbol
        qry = """SELECT *
                 FROM `stocks`.`companies`
                 WHERE
                    `symbol` = "%s";
              """ % self.symbol
        company_row = db.ex(qry)
        if len(company_row) <= 0:
            return None
        self.build_from_row(company_row[0])
        if full:
            self.load()
        return self

    def build_from_row(self, company_row):
        self.id = company_row[0]
        self.symbol = company_row[1]
        self.name = company_row[2]
        self.price = company_row[3]
        self.market_cap = company_row[4]
        self.ipo_year = company_row[5]
        self.sector = company_row[6]
        self.industry = company_row[7]
        self.exchange = company_row[8]
        self.high_52_weeks = company_row[9]
        self.high_52_weeks_date = company_row[10]
        self.low_52_weeks = company_row[11]
        self.low_52_weeks_date = company_row[12]
        self.run_company = company_row[13]
        self.ts_created = company_row[14]
        self.ts_updated = company_row[15]

    def save(self, save_none_vals=[]):
        if self.price in ['n/a']:
            self.price = None
        if self.sector in ['n/a']:
            self.sector = None
        data = {
            'symbol': self.symbol,
            'name': self.name,
            'price': self.price,
            'market_cap': self.market_cap,
            'ipo_year': self.ipo_year,
            'sector': self.sector,
            'industry': self.industry,
            'exchange': self.exchange,
            'high_52_weeks': self.high_52_weeks,
            'high_52_weeks_date': self.high_52_weeks_date,
            'low_52_weeks': self.low_52_weeks,
            'low_52_weeks_date': self.low_52_weeks_date,
            'run_company': self.run_company,
        }
        db.iodku(company_table, data)

    def save_meta(self, meta_info):
        meta_info['entity_id'] = self.id
        meta_info['entity_type'] = 'company'
        meta_info
        m.save(meta_info)

    def save_webhit(self):
        if 'meta' not in self.loaded:
            self.load()
        if 'web_hit' not in self.meta:
            m = {
                'meta_type': 'int',
                'meta_key': 'web_hit',
                'value': 1,
            }
        else:
            m = self.meta['web_hit']
            m['value'] = m['value'] + 1
        self.save_meta(m)

    def load(self):
        # self.load_quotes()
        self.load_meta()
        self.loaded = ['meta']

    def load_quotes(self, limit=31):
        qry = """
            SELECT * FROM `stocks`.`quotes`
            WHERE `company_id` = %s
            ORDER BY `quote_date` DESC
            LIMIT %s; """ % (self.id, limit)
        self.quotes = db.ex(qry)

    def load_meta(self):
        info = {}
        info['entity_id'] = self.id
        info['entity_type'] = 'company'
        self.meta = m.load(info)

# End File: stocks/modules/company.py
