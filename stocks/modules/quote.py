"""
    Quote Model

    QUOTE TABLE
    CREATE TABLE `quotes` (
        `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        `company_id` bigint(20) DEFAULT NULL,
        `day_high` decimal(20,4) DEFAULT NULL,
        `day_low` decimal(20,4) DEFAULT NULL,
        `current` decimal(20,4) DEFAULT NULL,
        `date` datetime DEFAULT NULL,
        PRIMARY KEY (`id`)
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
        self.day_high = None
        self.day_low = None
        self.day_avg = None
        self.current = None
        self.date = None

    def get_by_id(self, quote_id):
        self.id = quote_id
        qry = """SELECT *
                 FROM `stocks`.`quote`
                 WHERE
                    `id` = %s;
              """ % self.id
        q_row = db.ex(qry)
        print qry
        print 'q_row ROW'
        print q_row
        if len(q_row) <= 0:
            return None
        self.build_from_row(q_row[0])

    def build_from_row(self, quote_row):
        self.id = self.id
        self.company_id = quote_row[1]
        self.day_high = quote_row[2]
        self.day_low = quote_row[3]
        self.date = quote_row[4]
        self.current = quote_row[5]

    def save(self):
        if not self.id:
            if not self.date:
                self.date = datetime.now()
            insert_fields = []
            insert_vals = []
            insert_fields.append('company_id')
            insert_vals.append(self.company_id)
            if self.day_high:
                insert_fields.append('day_high')
                insert_vals.append(self.day_high)
            if self.day_high:
                insert_fields.append('day_low')
                insert_vals.append(self.day_low)
            if self.day_high:
                insert_fields.append('current')
                insert_vals.append(self.current)
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
            db.ex(qry)
            return True
