"""
    Company Model

    COMPANY TABLE
    CREATE TABLE `stocks`.`companies` (
      `id`                  bigint(20) unsigned NOT NULL AUTO_INCREMENT,
      `symbol`              varchar(10) DEFAULT NULL,
      `name`                varchar(255) DEFAULT NULL,
      `price`               decimal(20,4) DEFAULT NULL,
      `market_cap`          decimal(20,4) DEFAULT NULL,
      `ipo_year`            varchar(10) DEFAULT NULL,
      `sector`              varchar(255) DEFAULT NULL,
      `industry`            varchar(255) DEFAULT NULL,
      `exchange`            varchar(50) DEFAULT NULL,
      `high_52_weeks`       decimal(20,4) DEFAULT NULL,
      `high_52_weeks_date`  DATETIME DEFAULT NULL,
      `low_52_weeks`        decimal(20,4) DEFAULT NULL,
      `low_52_weeks_date`   DATETIME DEFAULT NULL,
      `run_company`         tinyint(1) DEFAULT NULL,
      `ts_update`           datetime DEFAULT NULL,
      PRIMARY KEY (`id`),
      KEY `symbol` (`symbol`)
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
        self.ts_update = None

    def __repr__(self):
        return '<Company %r, %r>' % (self.symbol, self.name)

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
        self.load()
        return self

    def build_from_row(self, company_row):
        self.id = company_row[0]
        self.symbol = company_row[1]
        self.name = company_row[2]
        self.price = company_row[3]
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
        self.ts_update = None

    def save(self, save_none_vals=[]):
        if self.price in ['n/a']:
            self.price = None

        if not self.id:
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
            db.insert(company_table, data)
        else:
            data = {}
            data['id'] = self.id
            if self.symbol:
                data['symbol'] = self.symbol
            if self.name:
                data['name'] = self.name
            if self.price:
                data['price'] = self.price
            if self.market_cap:
                data['market_cap'] = self.market_cap
            if self.ipo_year:
                data['ipo_year'] = self.ipo_year
            if self.sector:
                data['sector'] = self.sector
            if self.industry:
                data['industry'] = self.industry
            if self.exchange:
                data['exchange'] = self.exchange
            if self.high_52_weeks:
                data['high_52_weeks'] = self.high_52_weeks
            if self.high_52_weeks_date:
                data['high_52_weeks_date'] = self.high_52_weeks_date
            if self.low_52_weeks:
                data['low_52_weeks'] = self.low_52_weeks
            if self.low_52_weeks_date:
                data['low_52_weeks_date'] = self.low_52_weeks_date
            if self.run_company:
                data['run_company'] = self.run_company
            db.iodku(company_table, data)

    def load(self):
        self.load_meta()

    def load_meta(self):
        info = {}
        info['entity_id'] = self.id
        info['entity_type'] = 'company'
        self.meta = m.load(info)

    def save_meta(self, meta_info):
        meta_info['entity_id'] = self.id
        meta_info['entity_type'] = 'company'
        meta_info
        m.save(meta_info)
