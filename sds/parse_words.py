from politeauthority.driver_mysql import DriverMysql
from politeauthority import environmental
# import nltk
# from datetime import datetime

import pprint
import operator

mdb = DriverMysql(environmental.mysql_conf())
ignore_words = ['a', 'i', 'the']
remove_chars = ['!', '.', ',', ':']

sql = 'select * from `sds`.`raw_text`;'
tweets = mdb.ex(sql)
words = {}
for t in tweets:

    text = t[3]
    stext = text.split(' ')
    # tokens = nltk.word_tokenize(text)
    for w in stext:
        w = w.strip()
        for remove in remove_chars:
            w = w.replace(remove, '')
        if len(w) < 4:
            continue
        if w not in words:
            words[w] = 1
        else:
            words[w] = words[w] + 1
words = sorted(words.items(), key=operator.itemgetter(1))
print words
for w in words:
    print w
    # if c > 10:
        # print '%s: %s' % (c, w)
