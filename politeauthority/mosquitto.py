#!/usr/bin/env python
"""
    Mosquitto
"""

import paho.mqtt.publish as mpublish
from datetime import datetime
import ast

from politeauthority import environmental


class Mosquitto(object):

    def __init__(self, config=None):
        if not config:
            self.host = None
        else:
            self.host = config['host']

    def publish(self, topic, payload):
        if isinstance(payload, basestring):
            og_payload = payload
            payload = {
                'data': og_payload,
            }
        elif not payload:
            payload = {}
        # payload['machine_id'] = environmental.get_machine_id()
        # payload['date_recorded'] = datetime.now()
        payload = str(payload)
        mpublish.single(
            topic,
            payload,
            hostname=self.host)

    def parse_str_payload(self, payload_string):
        payload_dict = ast.literal_eval(payload_string)
        return payload_dict

    def find_machine_id(self, topic):
        if '/' in topic:
            last_segment = topic[topic.rfind('/')]
            return last_segment
        else:
            return None

    def consume_message(self, topic, payload):
        machine_id = self.find_machine_id(payload)
        if machine_id:
            machine_id = '"%s"' % machine_id
        else:
            machine_id = 'NULL'
        qry = """INSERT INTO `collectums`.`mqtt_raw`
            (machine_id, topic, message ,processed ,ready_to_delete) VALUES
            (%(machine_id)s, "%(topic)s", "%(message)s", 0, 1 );"""

        vals = {
            'machine_id': machine_id,
            'topic': topic,
            'message': payload
        }
        combined = qry % vals
        return combined

# EndFile: politeauthority/mosquitto.py
