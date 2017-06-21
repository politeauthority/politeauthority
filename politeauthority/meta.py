"""
    Generic Meta class for mysql

    from politeauthority.meta import Meta

    def save_meta(self, meta_info):
        # see Meta().save() for description on meta_info
        m = Meta()
        m.schema = 'stocks'
        meta_info['entity_id'] = self.id
        meta_info['entity_type'] = 'company'
        m.save(meta_info)



    Basic Load Example for a class

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
      `ts_update`      DATETIME ON UPDATE CURRENT_TIMESTAMP,
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
            Will insert, on duplicate keyt update. Keyed on key, entity_type, entity_id
            meta{
                'key':        varchar  REQUIRED UNIQUE KEY,
                'entity_type' varchar  REQUIRED UNIQUE KEY,
                'entity_id'   int      REQUIRED UNIQUE KEY,
                'meta_type'   varchar  REQUIRED UNIQUE KEY (decimal, int, varchar, text or datetime),
                'value':      basically any data type
                'id': int Optional,
            }
        """
        info = {
            'schema': self.schema,
            'table': self.table,
            'meta_key': '%s' % meta['meta_key'],
            'entity_type': meta['entity_type'],
            'entity_id': meta['entity_id'],
            'meta_type': meta['type'],
        }

        info['val_decimal'] = None
        info['val_int'] = None
        info['val_varchar'] = None
        info['val_text'] = None
        info['val_datetime'] = None
        info['val_list'] = None
        info['val_pickle'] = None
        if meta['type'] == 'decimal':
            info['val_decimal'] = meta['value']
        elif meta['type'] == 'int':
            info['val_int'] = meta['value']
        elif meta['type'] == 'varchar':
            info['val_varchar'] = db.escape_string(meta['value'])
        elif meta['type'] == 'text':
            info['val_text'] = db.escape_string(meta['value'])
        elif meta['type'] == 'datetime':
            info['val_datetime'] = meta['value']
        elif meta['type'] == 'list':
            if isinstance(meta['value'], list):
                value = '","'.join(meta['value'])
            else:
                value = meta['value']
            info['val_text'] = db.escape_string(value)
        elif meta['type'] == 'pickle':
            info['val_text'] = db.escape_string(cPickle.dumps(meta['value']))

        if info['val_list']:
            info['val_text'] = info['val_list']
        info.pop('val_list')
        info.pop('val_pickle')

        for field, item in info.iteritems():
            if field in ['schema', 'table']:
                continue
            if not item:
                info[field] = "NULL"
                continue
            if not isinstance(item, (int, long, float)):
                info[field] = '"%s"' % item
        qry = """INSERT INTO `%(schema)s`.`%(table)s`
                 (`meta_key`, `entity_type`, `entity_id`, `meta_type`, `val_decimal`, `val_int`, `val_varchar`,
                  `val_text`, `val_datetime`, `ts_update`)
                VALUES (%(meta_key)s, %(entity_type)s, %(entity_id)s, %(meta_type)s, %(val_decimal)s,
                    %(val_int)s, %(val_varchar)s, %(val_text)s, %(val_datetime)s, NOW())
                ON DUPLICATE KEY UPDATE `meta_type`=%(meta_type)s, `val_decimal`=%(val_decimal)s,
                    `val_int`=%(val_int)s, `val_varchar`=%(val_varchar)s, `val_text`=%(val_text)s,
                    `val_datetime`=%(val_datetime)s;"""
        db.ex(qry % info)

    def load_meta(self, meta, keys=[]):
        key_in_qry = ''
        if len(keys) > 0:
            key_in = '"%s",'.join(keys)
            key_in_qry = ' AND meta_key IN (%s)' % key_in
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
                'value': ret_value,
                'ts_created': m[10],
                'ts_updated': m[11],
            }
        return entity_meta

# End File politeauthority/politeauthority/meta.py
