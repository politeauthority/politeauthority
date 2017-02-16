#!/usr/bin/env python
"""
    Mosquitto
"""

import paho.mqtt.publish as mpublish

from politeauthority import environmental


class Mosquitto(object):

    def __init__(self, config):
        self.host = config['host']

    def publish(self, topic, payload):
        if isinstance(payload, basestring):
            og_payload = payload
            payload = {
                'data': og_payload,
            }
            print 'its a string'
        elif not payload:
            payload = {}
        payload['machine_id'] = environmental.get_machine_id()
        payload = str(payload)
        mpublish.single(
            topic,
            payload,
            hostname=self.host)

    def consume_publish(self, topic, payload):
        qry = """INSERT INTO `collectums`.`mqtt_raw` 
            (machine_id, topic, message ,processed ,ready_to_delete) VALUES
            (%(machine_id)s, %(topic)s, %(message)s, 0, 1 );"""
        vals = {
            'machine_id': self.find_machine_id(),
            'topic': topic,
            'payload': payload
        }
        combined = qry % vals
        print combined
        return

# EndFile: politeauthority/scan.py
