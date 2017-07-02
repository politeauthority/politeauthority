"""
    Quote Model

    QUOTE TABLE
    CREATE TABLE `stocks`.`quotes` (
        `id`            BIGINT(20) unsigned NOT NULL AUTO_INCREMENT,
        `company_id`    BIGINT(20) DEFAULT NULL,
        `open`          DECIMAL(20,4) DEFAULT NULL,
        `close`         DECIMAL(20,4) DEFAULT NULL,
        `high`          DECIMAL(20,4) DEFAULT NULL,
        `low`           DECIMAL(20,4) DEFAULT NULL,
        `volume`        BIGINT(20) DEFAULT NULL,
        `quote_date`    DATETIME DEFAULT NULL,
        `ts_created`    DATETIME DEFAULT CURRENT_TIMESTAMP,
        `ts_update`     DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (`id`),
        UNIQUE KEY `unique_index` (`company_id`, `quote_date`)
    );

"""
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

db = DriverMysql(environmental.mysql_conf())
company_table = 'stocks.quotes'


class Quote(object):

    def __init__(self):
        self.id = None
        self.company_id = None
        self.open = None
        self.close = None
        self.high = None
        self.low = None
        self.volume = None
        self.date = None

    def __repr__(self):
        return '<Quote %r, %r>' % (self.date, self.company_id)

    def get_by_id(self, quote_id):
        self.id = quote_id
        qry = """SELECT *
                 FROM `stocks`.`quote`
                 WHERE
                    `id` = %s;
              """ % self.id
        q_row = db.ex(qry)
        if len(q_row) <= 0:
            return None
        self.build_from_row(q_row[0])

    def build_from_row(self, quote_row):
        self.id = quote_row[0]
        self.company_id = quote_row[1]
        self.open = quote_row[2]
        self.close = quote_row[3]
        self.high = quote_row[4]
        self.low = quote_row[5]
        self.volume = quote_row[6]
        self.date = quote_row[7]
        return self

    def save(self):
        data = {
            'id': self.id,
            'company_id': self.company_id,
            'open': self.open,
            'close': self.close,
            'high': self.high,
            'low': self.low,
            'volume': self.volume,
            'quote_date': db.safe_date(self.date),
        }
        db.iodku(company_table, data)

# End File:
