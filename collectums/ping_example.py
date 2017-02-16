from politeauthority.mosquitto import Mosquitto

print Mosquitto

config = {}
config['host'] = 'chatsec.org'

m = Mosquitto(config).publish('testing!', 'testing')
