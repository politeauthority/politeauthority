#!/usr/bin/python
"""
 Mysql DB Driver
 This driver simplifies some of the MySQL interactions
 example usage
    from politeauthority,driver_mysql import DriverMysql
    db = DriverMysql(conf)
    db.ex('select * from `some_db`.`some_table`;')
    db.ex('inert into `some_db`.`some_table` (`thing`, `otherthing`) VALUES ('yeah', nah);')
    db.conn.close()
"""

import MySQLdb as mdb
from datetime import datetime


class DriverMysql(object):

    def __init__(self, database=None):
        if database:
            self.host = database['host']
            self.user = database['user']
            self.password = database['pass']
            self.port = int(database.get('port', 3306))
            self.dbname = database.get('name', '')
        self.create_conn()

    def create_conn(self):
        self.conn = mdb.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            port=self.port
        )

    def execute(self, query, getdict=False):
        return self.ex(query, getdict)

    def ex(self, query, kwargs=False):
        if not kwargs:
            kwargs = {}
        cur = self.conn.cursor()
        cur.execute(query, **kwargs)
        result = cur.fetchall()
        self.conn.commit()
        return result

    # insert
    # @params
    #   table  : str()
    #   items  : dict{ 'column' : 'value' }
    def insert(self, table, items):
        table = self.__format_db_table_sql(table)
        columns = []
        values = []
        for column, value in items.items():
            columns.append(column)
            values.append(value)
        column_sql = ''
        for column in columns:
            column_sql = column_sql + "`%s`," % column
        column_sql = column_sql.rstrip(column_sql[-1:])
        value_sql = ''
        for value in values:
            if value:
                value_sql += '"%s",' % self.escape_string(value)
            else:
                value_sql += "NULL,"
        value_sql = value_sql.rstrip(value_sql[-1:])

        sql = """INSERT INTO %s (%s) VALUES(%s);""" % (
            table, column_sql, value_sql)
        self.ex(sql)
        return sql

    def update(self, table, items, where, limit=1):
        table = self.__format_db_table_sql(table)
        set_sql = ''
        for column, value in items.items():
            set_sql = set_sql + '`%s`="%s", ' % (column, value)
        set_sql = set_sql.rstrip(set_sql[-2:])
        where_sql = ''
        for column, value in where.items():
            where_sql = where_sql + '`%s`="%s" AND ' % (column, value)
        where_sql = where_sql.rstrip(where_sql[-4:])

        sql = """UPDATE %s SET %s WHERE %s LIMIT %s;""" % (
            table, set_sql, where_sql, limit)
        # self.ex( sql )
        return sql

    def iodku(self, table, items):
        sep = self.__separate_items(items)
        cols = sep['columns']
        vals = sep['values']
        qry = """
                 INSERT INTO %(table)s
                    (%(columns)s)
                    VALUES (%(values)s)
                ON DUPLICATE KEY UPDATE
                    %(update_sql)s;""" % {
            'table': self.__format_db_table_sql(table),
            'columns': self.__sql_col(cols),
            'values': self.__sql_val(vals),
            'update_sql': self.__sql_update(cols, vals)
        }
        print qry
        self.ex(qry)
        return qry

    def __separate_items(self, items):
        columns = []
        values = []
        for column, value in items.items():
            columns.append(column)
            values.append(value)
        return {'columns': columns, 'values': values}

    def __sql_col(self, cols):
        sql = ''
        for c in cols:
            sql += "`%s`, " % c
        return sql[:-2]

    def __sql_val(self, vals):
        sql = ''
        for v in vals:
            if isinstance(v, int) or isinstance(v, float):
                sql += '%s, ' % v
            elif isinstance(v, datetime):
                sql += '"%s", ' % v
            else:
                sql += '"%s", ' % self.escape_string(v)
        return sql[:-2]

    def __sql_update(self, cols, vals):
        sql = ''
        for x in range(0, len(cols)):
            sql += """`%s` = "%s", """ % (cols[x], vals[x])
        return sql[:-2]

    def escape_string(self, string):
        return self.conn.escape_string(string)

    def alt_con(self, host, dbuser, dbpass, dbname=None, port=3306):
        self.host = host
        self.dbname = dbname
        self.user = dbuser
        self.password = dbpass
        self.port = int(port)
        return True

    def list_to_string(self, the_list):
        the_string = ''
        for item in the_list:
            the_string += '"%s", ' % item
        the_string = the_string[:-2]
        return the_string

    def __format_db_table_sql(self, db_or_table_or_both):
        if '.' in db_or_table_or_both:
            the_sql = db_or_table_or_both.split('.')
            pretty = """`%s`.`%s`""" % (the_sql[0], the_sql[1])
        else:
            if self.dbname != '':
                pretty = """`%s`.`%s`""" % (self.dbname, db_or_table_or_both)
            else:
                pretty = """`%s`""" % (db_or_table_or_both)
        return pretty

# End File: __/drivers/DriverMysql
