import paho.mqtt.client as mqtt
from config import config

from politeauthority.mosquitto import Mosquitto
from politeauthority.driver_mysql import DriverMysql

mconf = {
    'host': config['db_host'],
    'user': config['db_user'],
    'pass': config['db_pass']
}

mdb = DriverMysql(mconf)


class Consume(object):

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        client.subscribe("#")

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))
        print userdata
        print msg
        topic, machine_id = self.parse_topic(msg.topic)
        print topic
        print machine_id
        print msg.payload
        # self.determine_route(topic)
        # qry = self.consume_qry(msg.topic, msg.payload)
        # mdb.ex(qry)

    def parse_topic(self, topic):
        return [topic[:topic.find('/')], topic[topic.rfind('/') + 1:]]

    def determine_route(self, topic):
        if topic == 'net_nanny':
            print topic
        # print topic

    def consume_qry(self, topic, payload):
        machine_id = Mosquitto().find_machine_id(topic)
        if machine_id:
            machine_id = '"%s"' % machine_id
        else:
            machine_id = 'NULL'
        qry = """INSERT INTO `collectums`.`mqtt_raw`
            (machine_id, topic, processed ,ready_to_delete) VALUES
            (%(machine_id)s, "%(topic)s", 0, 1 );"""

        vals = {
            'machine_id': machine_id,
            'topic': topic,
            'message': payload
        }
        combined = qry % vals
        return combined


if __name__ == "__main__":
    consumer = Consume()
    client = mqtt.Client()
    client.on_connect = consumer.on_connect
    client.on_message = consumer.on_message
    client.connect("chatsec.org", 1883, 60)
    client.loop_forever()
