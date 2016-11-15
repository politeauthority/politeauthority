from politeauthority.driver_mysql import DriverMysql
import nltk
from datetime import datetime

import twitter
import pprint

db_host = 'chatsec.org'
db_user = 'devel'
db_pass = '78VWc_bKTAap'

mconf = {
    'host': db_host,
    'user': db_user,
    'pass': db_pass
}
mdb = DriverMysql(mconf)

sql = 'select * from `sds`.`raw_text`;'
tweets = mdb.ex(sql)
words = {}
for t in tweets:

    text = t[3]
    stext = text.split(' ')
    tokens = nltk.word_tokenize(text)
    # for w in stext:
    #     if w not in words:
    #         words[w] = 1
    #     else:
    #         words[w] = words[w] + 1

for w, c in words.iteritems():
    if c > 10:
        print '%s: %s' % (c, w)
