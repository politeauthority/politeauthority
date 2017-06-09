"""
    META TABLE
    CREATE TABLE `meta` (
      `meta_id`        BIGINT(20) unsigned NOT NULL AUTO_INCREMENT,
      `key`            VARCHAR(50) DEFAULT NULL,
      `entity_type`    VARCHAR(10) DEFAULT NULL,
      `entity_id`      VARCHAR(255) DEFAULT NULL,
      `meta_type`      VARCHAR(10) DEFAULT NULL,
      `val_decimal`    DECIMAL(20,2) DEFAULT NULL,
      `val_int`        BIGINT(40) DEFAULT NULL,
      `val_varchar`    VARCHAR(255) DEFAULT NULL,
      `val_text`       TEXT DEFAULT NULL,
      `val_datetime`   DATETIME DEFAULT NULL,
      `ts_created`     DATETIME DEFAULT CURRENT_TIMESTAMP,
      `ts_update` DATETIME ON UPDATE CURRENT_TIMESTAMP,
      PRIMARY KEY (`meta_id`),
      UNIQUE KEY `unique_index` (`key`,`entity_type`,`entity_id`)
    )
"""
from datetime import datetime

from politeauthority import environmental
from politeauthority.driver_mysql import DriverMysql

db = DriverMysql(environmental.mysql_conf())


class Meta(object):

    def __init__(self):
        self.schema = None
        self.table = 'meta'

    def save(self, meta):
        if 'id' not in meta:
            meta['id'] = None
        info = {
            'schema': self.schema,
            'table': self.table,
            'meta_id': meta['id'],
            'key':  '%s' % meta['key'],
            'entity_type': 'company',
            'entity_id': meta['entity_id'],
            'meta_type': meta['type'],
        }
        if meta['type'] == 'decimal':
            info['val_decimal'] = meta['value']
        else:
            info['val_decimal'] = None
        if meta['type'] == 'int':
            info['val_int'] = meta['value']
        else:
            info['val_int'] = None
        if meta['type'] == 'varchar':
            info['val_varchar'] = db.escape_string(meta['value'])
        else:
            info['val_varchar'] = None
        if meta['type'] == 'text':
            info['val_text'] = db.escape_string(meta['value'])
        else:
            info['val_text'] = None
        if meta['type'] == 'datetime':
            info['val_datetime'] = db.escape_string(meta['value'])
        else:
            info['val_datetime'] = None

        for field, item in info.iteritems():

            if field in ['schema', 'table']:
                continue
            if not item:
                info[field] = "NULL"
                continue
            if isinstance(item, basestring) or isinstance(item, datetime):
                info[field] = '"%s"' % item

        qry = """INSERT INTO `%(schema)s`.`%(table)s`
                 (`key`, `entity_type`, `entity_id`, `meta_type`, `val_decimal`, `val_int`, `val_varchar`,
                  `val_text`, `val_datetime`, `ts_update`)
                VALUES (%(key)s, %(entity_type)s, %(entity_id)s, %(meta_type)s, %(val_decimal)s,
                    %(val_int)s, %(val_varchar)s, %(val_text)s, %(val_datetime)s, NOW())
                ON DUPLICATE KEY UPDATE `meta_type`=%(meta_type)s, `val_decimal`=%(val_decimal)s, `val_int`=%(val_int)s,
                  `val_varchar`=%(val_varchar)s, `val_text`=%(val_text)s, `val_datetime`=%(val_datetime)s"""
        db.ex(qry % info)

    def load_meta(self, meta, keys=[]):
        key_in_qry = ''
        if len(keys) > 0:
            key_in = '"%s",'.join(keys)
            key_in_qry = ' AND key IN (%s)' % key_in
        qry = """SELECT * FROM `%s`.`%s`
                 WHERE
                    `entity_type`="%s"
                    AND
                    `entity_id`=%s
                    %s; """ % (
                        self.schema,
                        self.table,
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

            entity_meta[m_key] = {
                'meta_id': m[0],
                'key': m_key,
                'entity_type': m[2],
                'value': m[val_field],
                'ts_created': m[10],
                'ts_updated': m[11],
            }
        return entity_meta

# End File politeauthority/politeauthority/meta.py
