"""
    Stocks.py

    example stock sample
        vslr = {
        'symbol': 'VSLR',
        'purchases': [{
            'price': 2.80,
            'shares': 2,
            'date': datetime(2017, 4, 19),
        }]
}
"""

from modules import load_portfolio as lp
import requests
import nltk
import praw

the_text = """Azethoth666 wrote: fic wrote: Peevester wrote: I think this will end up happening regardless of what rules Cheeto tries to eliminate. Hybrids and EVs are here to stay, by 2025 they'll just be \"cars\". \n\nAgreed. Just look at the effect he has had on coal plant closings - \"only\" 45 announcements of closing in the next 2 years. Including the biggest west of the Mississippi.\n\nThe Tesla Model 3 is a game changer - it will destroy the low end lines of BMW and Mercedes and the mid to upper of GM and Ford. It is only how fast Tesla can ramp production.\nThe Tesla and Workhorse W-15 pickups will come after their yuge profits in pickups.\nTesla battery costs will start at $125ish/kWh and drop below $100/kWh in a year or two.\nGM and BMW have basically dipped their little toe in the PHEV/EV market (I own a Volt), but Ford has basically only got a couple of drops on their toenail.\nToyota basically wants nothing to do with EV even after their huge success with the Prius.\nHonda? Mercedes? Chrysler? \nMercedes is building a gigafactory... or something large scale and going into power walls as well. Cannot recall if they have hopped on the solar thing yet or not. \n\nYeah, they announced a $500M investment in a factory - 1/10 the investment Tesla is putting into their first (of 5?) Gigafactories. They have partnered with Vivent for home energy storage."""


# def search_reddit():
#     r = praw.Reddit(user_agent='Getting the data!!',
#                     client_id='Knu5ZldshTE_fg',
#                     client_secret='UGZJmNcPKU7mAdw_0btc_BUYqNE',
#                     )
#     help(r.search)
#     results = r.search('whatever', subreddit=None, sort=None, syntax=None, period=None)
#     for x in results:
#         print x


def parse_words():
    search_phrases = ['Vivent', 'solar', 'VSLR']
    sentances = nltk.sent_tokenize(the_text)
    for sentance in sentances:
        for phrase in search_phrases:
            if phrase in sentance:
                words = nltk.word_tokenize(sentance)
                word_tokens = nltk.pos_tag(words)
                for word in word_tokens:
                    if word[1] in ['JJ', 'RB']:
                        print word[0]
                # print word_tokens
    # print sentances


def search_webhose():
    token = "0168aba8-3dca-43e8-81f7-f6e4a258c69f"
    base_url = "http://webhose.io/filterWebContent"
    args = {
        'token': token,
        'format': 'json',
        'q': 'vivent solar language:english'
    }
    print base_url
    r = requests.get(base_url,  params=args)
    if r.status_code != 200:
        print 'Error: Status Code %s' % r.status_code
        return False
    print r.text

if __name__ == '__main__':
    stocks = lp.load_portfolio_from_csv()
    # search_reddit()
    parse_words()
    # search()

# End File: politeauthority/stocks/search_news.py
