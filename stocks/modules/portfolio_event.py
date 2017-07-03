"""
    Portfolio Events Model

    Portfolio Events Table
    CREATE TABLE `stocks`.`portfolio_events` (
      `id`                  BIGINT(20) unsigned NOT NULL AUTO_INCREMENT,
      `portfolio_id`         BIGINT(20) DEFAULT NULL,
      `company_id`          BIGINT(20) DEFAULT NULL,
      `price`               DECIMAL(20,4) DEFAULT NULL,
      `count`               INT(10) DEFAULT NULL,
      `date`                DATETIME DEFAULT NULL,
      `type`                VARCHAR(10) DEFAULT NULL,
      `ts_created`          DATETIME DEFAULT CURRENT_TIMESTAMP,
      `ts_updated`          DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      KEY `portfolio_id` (`portfolio_id`)
    );


"""
from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

db = DriverMysql(environmental.mysql_conf())
portfolio_events_table = 'stocks.portfolio_events'


class PortfolioEvent(object):

    def __init__(self):
        self.id = None
        self.portfolio_id = None
        self.company_id = None
        self.price = None
        self.count = None
        self.date = None
        self.type = None
        self.ts_updated = None
        self.ts_created = None

    def __repr__(self):
        return '<PortfolioEvent %r, %r>' % (self.id, self.company_id)

    def get_by_portfolio_id(self, portfolio_id):
        self.portfolio_id = portfolio_id
        qry = """SELECT *
                 FROM `stocks`.`portfolio_events`
                 WHERE
                    `portfolio_id` = %s
                ORDER BY `date` DESC;
              """ % self.portfolio_id
        q_row = db.ex(qry)
        if len(q_row) <= 0:
            return None
        self.build_from_row(q_row[0])
        return self

    def build_from_row(self, event_row):
        self.id = event_row[0]
        self.portfolio_id = event_row[1]
        self.company_id = event_row[2]
        self.price = event_row[3]
        self.count = event_row[4]
        self.date = event_row[5]
        self.type = event_row[6]
        self.ts_updated = event_row[7]
        self.ts_created = event_row[8]
        return self

    def save(self, save_none_vals=[]):
        data = {
            'portfolio_id': self.portfolio_id,
            'company_id': self.company_id,
            'price': self.price,
            'count': self.count,
            'date': self.date,
            'type': self.type,
            'ts_updated': self.ts_updated,
            'ts_created': self.ts_created,
        }
        print db.iodku(portfolio_events_table, data)

    def load(self):
        pass

# End File: stocks/modules/portfolio_event.py
