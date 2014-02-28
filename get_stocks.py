import requests
import json


def get_quote(sym):
    url = 'http://dev.markitondemand.com/Api/v2/Quote/json'
    parameters = {'symbol': sym}
    resp = requests.get(url, params=parameters)
    resp.raise_for_status()
    data = json.loads(resp.text)
    symbol = data['Symbol']
    close = data['LastPrice']
    time = data['Timestamp']
    return (symbol, close, time)


def btc_last():
    api_url = 'https://api.bitcoinaverage.com/ticker/global/USD/'
    resp = requests.get(api_url)
    resp.raise_for_status()
    data = json.loads(resp.text)
    bt = data['last']
    return bt


def combine():
    symbol, close, time = get_quote('tsla')
    bitcoin = btc_last()
    return "%s\r\n%s: %.6f BTC" % (
        time.encode('utf-8'),
        symbol.encode('utf-8'),
        (close / bitcoin)
    )


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8000, combine)
    srv.serve_forever()
