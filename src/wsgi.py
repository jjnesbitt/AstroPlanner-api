import main as forecast
import urllib

def application(environ, start_response):
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    start_response('200 OK', [('Content-Type', 'application/json')])
    return forecast.main(params).encode('utf-8')
