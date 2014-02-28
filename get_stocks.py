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


def application(environ, start_response):
    headers = [("Content-type", "text/html")]
    # body = combine()
    # headers.append(('Content-length', str(len(body))))
    # start_response('200 OK', headers)
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        body = combine()
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]
    return [body]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8000, application)
    srv.serve_forever()
