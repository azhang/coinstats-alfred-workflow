# -*- coding: utf-8 -*-
import json
import locale
import sys
import urllib2

locale.setlocale(locale.LC_ALL, locale.getdefaultlocale())


#CURRENCY_SYMBOL = locale.localeconv()['int_curr_symbol'].lower().strip() or 'usd'
#override with eth
CURRENCY_SYMBOL = 'eth'

def make_response():
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0&convert={}'.format(CURRENCY_SYMBOL)
    try:
        response = urllib2.urlopen(url).read()
        data = json.loads(response)
        return sorted(data, key=lambda x: int(x['rank']))
    except Exception:
        return []


def make_item(coin):
    #price_key = 'price_{}'.format(CURRENCY_SYMBOL)
    price_key = 'price_usd'
    market_cap_key = 'market_cap_{}'.format(CURRENCY_SYMBOL)
    coin['price_eth'] = u"Ξ{}".format(coin['price_eth'])
    if not coin[price_key]:
        coin['price'] = 'null'
    else:
        coin['price'] = locale.currency(float(coin[price_key]), grouping=True)
    if not coin[market_cap_key]:
        coin['market_cap'] = 'null'
    else:
        coin['market_cap'] = locale.currency(float(coin[market_cap_key]), grouping=True)
    return {
        'uid': coin['rank'],
        'title': u"{} - {} - {} | {}".format(coin['name'], coin['symbol'], coin['price'], coin['price_eth']),
        'subtitle': 'Market cap: {}'.format(coin['market_cap']),
        'type': 'default',
        'icon': {
            'path': './icons/{}.png'.format(coin['symbol'].lower())
        },
        'arg': coin['id']
    }


def filter_data(data, query):
    def fun(x):
        q = query.lower()
        name = x['name'].lower()
        symbol = x['symbol'].lower()
        return q in name or q in symbol
    return list(filter(fun, data))


def output(data):
    return {
        'items': list(map(make_item, data))
    }


data = make_response()

if len(sys.argv) == 1:
    sys.stdout.write(json.dumps(output(list(data))))
else:
    query = sys.argv[1]
    sys.stdout.write(json.dumps(output(filter_data(data, query))))
