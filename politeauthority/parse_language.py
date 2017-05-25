"""
    Parse Language

    create table lang.translations(
        translation_id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        translation_name varchar(255) default null,
        translation_description text default null,
        PRIMARY KEY (`translation_id`) );

    create table lang.term_relationships(
        id bigint(20) unsigned NOT NULL AUTO_INCREMENT,
        term_id bigint(20) not null,
        translation_id bigint(20) not null,
        PRIMARY KEY (`id`) );

    create table lang.terms(
        term_id bigint(20) unsigned  NOT NULL AUTO_INCREMENT,
        term varchar(255) default null,
        term_type varchar(255) default null,
        PRIMARY KEY (`term_id`) );
"""


import string


def translation_sets(term_type):
    qry = """SELECT *
             FROM `lang`.`terms` t
             JOIN `lang`.`term_relationshops` tr
                ON t.`term_id` = tr.term_id
            JOIN `lang`.`translations` trans
                ON trans.translation_id=tr.translation_id
             WHERE
                t.term_type = "%s" ;""" % term_type


def hash_tags(_string):
    return {tag.strip("#") for tag in _string.split() if tag.startswith("#")}


def at_mentions(_string):
    if ' ' not in _string:
        words = [_string]
    else:
        words = _string.split()
    if '' in words:
        words.remove('')
    d = {}
    for word in _string:
        if word.startswith("@"):
            key = "@" + word.translate(None, string.punctuation).lower()
            if key not in d:
                d[key] = 0
            d[key] += 1
    return d

common_missspellings = {
    'absence': ['absense, absance'],
    'acceptable': ['acceptible'],
    'accidentally': ['accidentaly'],
    'accommodate': ['accomodate, acommodate'],
    'achieve': ['acheive'],
    'acknowledge': ['acknowlege', 'aknowledge'],
    'acquaintance': ['acquaintence', 'aquaintance'],
    'acquire': ['aquire', 'adquire'],
    'acquit': ['aquit'],
    'acreage': ['acrage', 'acerage'],
    'address': ['adress'],
    'adultery': ['adultary'],
    'advisable': ['adviseable', 'advizable'],
    'affect': ['effect'],
    'aggression': ['agression'],
    'aggressive': ['agressive'],
    'allegiance': ['allegaince', 'allegience', 'alegiance'],
    'almost': ['allmost'],
    'a lot': ['alot'],
    'amateur': ['amatuer', 'amature'],
    'annually': ['anually', 'annualy'],
    'apparent': ['apparant'],
    'arctic': ['artic'],
    'argument': ['arguement'],
    'atheist': ['athiest'],
    'awful': ['awfull', 'aweful'],
    'because': ['becuase'],
    'becoming': ['becomeing'],
    'beginning': ['begining'],
    'believe': ['beleive'],
    'bellwether': ['bellweather'],
    'buoy': ['bouy'],
    'buoyant': ['bouyant'],
    'business': ['buisness'],
    # https://en.wikipedia.org/wiki/Commonly_misspelled_English_words#cite_note-YD-4
}

lingo_twitter = {
     "About": ["AB", "ABT"],
     "As far as I know": ["AFAIK"],
     "Are you fucking kidding me with this shit?": ["AYFKMWTS"],
     "Before": ["B4"],
     "Bye for now": ["BFN"],
     "Background": ["BGD"],
     "Blockhead": ["BH"],
     "Best regards": ["BR"],
     "By the way": ["BTW"],
     "Code 9, parents are around": ["CD9"],
     "Check": ['CHK'],
     "See you later": ['CUL8R'],
     "Don’t annoy me": ['DAM'],
     "Dear daughter": ['DD'],
     "Dear fiancé": ['DF'],
     "used to mean “profile pic”": ['DP'],
     "Dear son": ['DS'],
     "Did you know?": ["DYK"],
     "Email": ["EM", "EML"],
     "Email address": ["EMA"],
     "Face to face": ["F2F", "FTF"],
     "Facebook, F--- buddy": ["FB"]
     # "Follow Friday": FF =
     # "For Fucks‘s Sake": ["FFS"]
     # "F--- my life.": ["FML"]
     # "Find of the day": ["FOTD"]
     # "For the win": ["FTW"],
     # "F---ed up beyond all repair": ["FUBAR"]
     # "For what it's worth.": FWIW =
     # "Give me a f---ing break": GMAFB =
     # "Get the f--- out of here": GTFOOH =
     # "Guess the song": GTS =
     # "Have a good night": HAGN =
     # "Have a nice day": HAND =
     # "Headline of the day": HOTD =
     # "Heard through": HT =
     # "Hope that helps": HTH =
     # "I see": IC =
     # ""In case you missed it," a quick way to apologize for retweeting your own material": ICYMI =
     # "I don't know": IDK =
     # "If I remember correctly": IIRC =
     # "In my humble opinion.": IMHO =
     # "In real life": IRL =
     # "I want sex now": IWSN =
     # "Just kidding, joke": JK =
     # "Just so you know": JSYK =
     # "Joint venture": JV =
     # "Kewl kewl, or ok, got it": KK =
     # "Knock your socks off": KYSO =
     # "Laugh hella hard (stronger version of LOL)": LHH =
     # "Laughing my ass off": LMAO =
     # "Let me know": LMK =
     # "Little One (child)": LO =
     # "Laugh out loud": LOL =
     # "Music Monday": MM =
     # "Meet in real life": MIRL =
     # "Marijuana": MRJN =
     # "No big deal": NBD =
     # "Nobody cares, though": NCT =
     # "No f---ing way": NFW =
     # "Enjoy": NJoy =
     # "Not safe for work": NSFW =
     # "Note to self": NTS =
     # "Overheard": OH =
     # "Oh my f---ing God": OMFG =
     # "One of my friends/followers": OOMF =
     # "Oh, really?": ORLY =
     # "Please let me know": PLMK =
     # "Party and Play (drugs and sex)": PNP =
     # "quote of the day": QOTD =
     # "In reply to, in regards to": RE =
     # "Real-life re-tweet, a close cousin to OH": RLRT =
     # "Read the f---ing manual": RTFM =
     # "Read the question": RTQ =
     # "Safe for work": SFW =
     # "Shaking my damn head, SMH, only more so": SMDH =
     # "Shaking my head": SMH =
     # "Situation normal, all f---ed up (slang from the US Military)": SNAFU =
     # "Significant Other": SO =
     # "Son of a B----": SOB =
     # "Serious": SRS =
     # "Shut the f--- up!": STFU =
     # "Search the f---ing web!": STFW =
     # "Thanks for the follow": TFTF =
     # "Thanks for this tweet": TFTT =
     # "Tweetjack, or joining a conversation belatedly to contribute to a tangent": TJ =
     # "Timeline": TL =
     # Too long, didn’t read": TLDR/TL";DR  =
     # "Tweet me back": TMB =
     # "Trending topic": TT =
     # "Thank you": TY =
     # "Thank you in advance": TYIA =
     # "Take your time": TYT =
     # "Thank you very much": ["TYVW"],
     # "With": ["W", "W/"],
     # Whatever or weekend": W/E "or WE =
     # "Whatever": WTV =
     # "You got that right": YGTR =
     # "You know what I mean": YKWIM =
     # "You know you're addicted to": YKYAT =
     # "Your mileage may vary": YMMV =
     # "You only live once": YOLO =
     # "You're on your own": YOYO =
     # "You're welcome": YW =
     # "OMG to the max": ZOMG =
}
