from politeauthority.driver_mysql import DriverMysql
from datetime import datetime
import twitter
import pprint
import sys
from config import config

mconf = {
    'host': config['db_host'],
    'user': config['db_user'],
    'pass': config['db_pass']
}
mdb = DriverMysql(mconf)

consumer_key = "4lxB1IJYLBoH5MRn6889jvF7B"
consumer_secret = "bsQLCHElUrhzC5Eoiy1K3ZQz3PJSTC0idxSxn6uAQGuIjIQyIe"
access_key = "9213842-thUhVewPIyyMVtAsvo8P1MEYhA03IJ3dXdrCjq2zoN"
access_secret = "n9lgTLB6Z4R8HrGt7iGDbOwZat2gP8D6EpPJu617gfxaf"


def insert(source, created_at, text):
    text = text.replace('"', '\\"')
    qry = """SELECT * FROM `sds`.`raw_text` WHERE `text`="%s";""" % text
    exists = mdb.ex(qry)
    if len(exists) > 0:
        print 'Already exits'
        return
    qry = """INSERT INTO `sds`.`raw_text` (`source`, `date`, `text`)
        VALUES("%s", "%s", "%s");""" % (
        source,
        created_at,
        text
    )
    mdb.ex(qry)
    mdb.conn.commit()
    print "Saved"


def twitter_to_time(twitter_time):
    tt = datetime.strptime(twitter_time, '%a %b %d %H:%M:%S +0000 %Y')
    return tt

tw = twitter.Twitter(auth=twitter.OAuth(
    access_key,
    access_secret,
    consumer_key,
    consumer_secret))

results = tw.statuses.user_timeline(
    screen_name='realDonaldTrump',
    max_id=sys.argv[1],
    count=200)
pp = pprint.PrettyPrinter(indent=4)

for status in results:
    print "(%s) %s" % (status["created_at"], status["text"].encode("ascii", "ignore"))
    # pp.pprint(status)
    tt = twitter_to_time(status['created_at'])
    insert('twitter', tt, status["text"].encode("ascii", "ignore"))
    print status['id']
    print '\n'
print ''
print len(results)


# End File
