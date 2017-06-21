"""
    Quote Model

    QUOTE TABLE
    CREATE TABLE `stocks`.`quotes` (
        `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        `company_id` bigint(20) DEFAULT NULL,
        `open` decimal(20,4) DEFAULT NULL,
        `close` decimal(20,4) DEFAULT NULL,
        `high` decimal(20,4) DEFAULT NULL,
        `low` decimal(20,4) DEFAULT NULL,
        `volume` bigint(20) DEFAULT NULL,
        `date` datetime DEFAULT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY `unique_index` (`company_id`, `date`)
    );

"""
from datetime import datetime

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

db = DriverMysql(environmental.mysql_conf())


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
        self.id = self.id
        self.company_id = quote_row[1]
        self.open = quote_row[2]
        self.close = quote_row[3]
        self.high = quote_row[4]
        self.low = quote_row[5]
        self.volume = quote_row[6]
        self.date = quote_row[7]

    def save(self):
        if not self.id:
            if not self.date:
                self.date = datetime.now()
            insert_fields = []
            insert_vals = []
            insert_fields.append('company_id')
            insert_vals.append(self.company_id)
            if self.open:
                insert_fields.append('open')
                insert_vals.append(self.open)
            if self.close:
                insert_fields.append('close')
                insert_vals.append(self.close)
            if self.high:
                insert_fields.append('high')
                insert_vals.append(self.high)
            if self.high:
                insert_fields.append('low')
                insert_vals.append(self.low)
            if self.volume:
                insert_fields.append('volume')
                insert_vals.append(self.volume)
            if self.date:
                insert_fields.append('date')
                insert_vals.append(self.date)

            if len(insert_fields) == 0:
                return False

            ins_f = ''
            for f in insert_fields:
                ins_f += """`%s`, """ % f
            ins_f = ins_f[:-2]

            ins_v = ''
            for f in insert_vals:
                ins_v += """"%s", """"" % f

            ins_v = ins_v[:-2]
            qry = """INSERT INTO `stocks`.`quotes`
                     (%s)
                     VALUES
                     (%s);""" % (
                ins_f,
                ins_v
            )
            try:
                db.ex(qry)
            except Exception, e:
                print e
            return True
