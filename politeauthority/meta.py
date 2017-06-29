"""
    Generic Meta class for MySQL

    This Class can store and retrieve info for multiple entities, and multiple data types.
        Currently supports decimal, int, varchar, datetime, pickle and list

    Example Usage

    # Basic save example
    from politeauthority.meta import Meta

    def save_meta(meta_info):
        # see Meta().save() for description on meta_info
        m = Meta()
        m.schema = 'stocks'
        meta_info['entity_id'] = 2
        meta_info['entity_type'] = 'company'
        meta_info['meta_key'] = 'cool_info'
        meta_info['meta_type'] = 'pickle'
        meta_info['value'] = {'some': 'things'}
        m.save(meta_info)


    # Basic Load Example for a class

    from politeauthority.meta import Meta

    def load_meta(self):
        m = Meta()
        m.schema = 'stocks'
        info = {}
        info['entity_id'] = self.id
        info['entity_type'] = 'company'
        self.meta = m.load_meta(info)

    SQL Table
    CREATE TABLE `meta` (
      `id`             BIGINT(20) unsigned NOT NULL AUTO_INCREMENT,
      `meta_key`       VARCHAR(50) DEFAULT NULL,
      `entity_type`    VARCHAR(10) DEFAULT NULL,
      `entity_id`      VARCHAR(255) DEFAULT NULL,
      `meta_type`      VARCHAR(10) DEFAULT NULL,
      `val_decimal`    DECIMAL(20,2) DEFAULT NULL,
      `val_int`        BIGINT(40) DEFAULT NULL,
      `val_varchar`    VARCHAR(255) DEFAULT NULL,
      `val_text`       TEXT DEFAULT NULL,
      `val_datetime`   DATETIME DEFAULT NULL,
      `ts_created`     DATETIME DEFAULT CURRENT_TIMESTAMP,
      `ts_updated`      DATETIME ON UPDATE CURRENT_TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      PRIMARY KEY (`id`),
      UNIQUE KEY `unique_index` (`meta_key`, `entity_type`, `entity_id`)
    );
"""
import cPickle

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

db = DriverMysql(environmental.mysql_conf())


class Meta(object):

    def __init__(self):
        self.schema = None
        self.table = 'meta'

    def save(self, meta):
        """
        @desc:  Will save values into meta table with the correct stoage type and keying.
        @param: meta    (dict)
                    id              (int)
                    meta_key        (str) REQUIRED  meta field name
                    entity_type     (str) REQUIRED  type of object
                    entity_id       (str) REQUIRED  id of object
                    meta_type       (str) REQUIRED  type of storage
                                        Options: ('decimal', 'int', 'varchar', 'datetime', 'pickle', 'list')
                    value           (str||int||float||datetime||dict||list)
        """
        if not self.schema:
            raise Exception('Table schema REQUIRED')
        if 'meta_key' not in meta:
            raise Exception('`meta_key` REQUIRED')
        if 'meta_type' not in meta:
            raise Exception('`meta_type` REQUIRED')
        if 'entity_id' not in meta:
            raise Exception('`entity_id` REQUIRED')
        if 'entity_type' not in meta:
            raise Exception('`entity_type` REQUIRED')
        self.__table()
        meta['val_decimal'] = None
        meta['val_int'] = None
        meta['val_varchar'] = None
        meta['val_text'] = None
        meta['val_datetime'] = None
        if meta['meta_type'] == 'decimal':
            meta['val_decimal'] = meta['value']
        elif meta['meta_type'] == 'int':
            meta['val_int'] = meta['value']
        elif meta['meta_type'] == 'varchar':
            meta['val_varchar'] = db.escape_string(meta['value'])
        elif meta['meta_type'] == 'text':
            meta['val_text'] = db.escape_string(meta['value'])
        elif meta['meta_type'] == 'datetime':
            meta['val_datetime'] = meta['value']
            if meta['val_datetime'] and len(str(meta['val_datetime'])) > 19:
                meta['val_datetime'] = str(meta['val_datetime'])[:19]
        elif meta['meta_type'] == 'list':
            if isinstance(meta['value'], list):
                value = '"%s"' % '", "'.join(meta['value'])
            else:
                value = meta['value']
            meta['val_text'] = db.escape_string(value)
        elif meta['meta_type'] == 'pickle':
            meta['val_text'] = cPickle.dumps(meta['value'])
        data = {}
        m_fields = ['id', 'meta_key', 'entity_type', 'entity_id', 'meta_type', 'val_decimal',
                    'val_int', 'val_varchar', 'val_text', 'val_datetime']
        for x, y in meta.iteritems():
            if y and x in m_fields:
                data[x] = y
        db.iodku(self.meta_table, data)

    def load(self, meta, keys=[]):
        self.__table()
        key_in_qry = ''
        if len(keys) > 0:
            key_in = '"%s",'.join(keys)
            key_in_qry = ' AND meta_key IN (%s)' % key_in
        qry = """SELECT *
                 FROM %s
                 WHERE
                    `entity_type`="%s"
                    AND
                    `entity_id`=%s
                    %s; """ % (
            self.meta_table,
            meta['entity_type'],
            meta['entity_id'],
            key_in_qry)
        meta = db.ex(qry)
        entity_meta = {}
        for m in meta:
            m_key = m[1]
            m_type = m[4]
            val_field = ''
            if m_type == 'decimal':
                val_field = 5
            elif m_type == 'int':
                val_field = 6
            elif m_type == 'varchar':
                val_field = 7
            elif m_type == 'text':
                val_field = 8
            elif m_type == 'datetime':
                val_field = 9
            elif m_type == 'list':
                val_field = 8
            elif m_type == 'pickle':
                val_field = 8

            ret_value = m[val_field]

            # Handle special loads
            if m_type == 'list':
                ret_value = ret_value.split(',')
            elif m_type == 'pickle':
                if ret_value:
                    ret_value = cPickle.loads(ret_value)

            entity_meta[m_key] = {
                'id': m[0],
                'meta_key': m_key,
                'entity_type': m[2],
                'meta_type': m[4],
                'value': ret_value,
                'ts_created': m[10],
                'ts_updated': m[11],
            }
        return entity_meta

    def __table(self):
        if not self.schema:
            self.meta_table = self.table
        else:
            self.meta_table = "%s.%s" % (self.schema, self.table)

# End File politeauthority/politeauthority/meta.py
