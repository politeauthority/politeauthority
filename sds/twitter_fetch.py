from politeauthority.driver_mysql import DriverMysql
from politeauthority import environmental
from datetime import datetime
import twitter
import pprint
import sys

mconf = environmental.mysql_conf()
mdb = DriverMysql(mconf)

consumer_key = environmental.twitter_consumer_key()
consumer_secret = environmental.twitter_consumer_secret()
access_key = environmental.twitter_access_key()
access_secret = environmental.twitter_access_secret()


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

print len(sys.argv)
if len(sys.argv) > 1:
    results = tw.statuses.user_timeline(
        screen_name='realDonaldTrump',
        max_id=sys.argv[1],
        count=200)
else:
    results = tw.statuses.user_timeline(
        screen_name='realDonaldTrump',
        max_id=None,
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
