import ipgetter

from politeauthority.mosquitto import Mosquitto


config = {}
config['host'] = 'chatsec.org'


def main():
    payload = generate_payload()
    Mosquitto(config).publish('report_in', payload)


def get_wan_ip():
    IP = ipgetter.myip()
    return IP


def generate_payload():
    p = {}
    p['data'] = {}
    p['data']['wan_ip'] = get_wan_ip()
    return p

if __name__ == "__main__":
    main()
