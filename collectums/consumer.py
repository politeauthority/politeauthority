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
        qry = Mosquitto(config={}).consume_publish(msg.topic, msg.payload)
        mdb.ex(qry)


if __name__ == "__main__":
    consumer = Consume()
    client = mqtt.Client()
    client.on_connect = consumer.on_connect
    client.on_message = consumer.on_message
    client.connect("chatsec.org", 1883, 60)
    client.loop_forever()
