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

# EndFile: politeauthority/scan.py
