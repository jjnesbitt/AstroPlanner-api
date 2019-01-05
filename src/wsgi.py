import main as forecast
import urllib

def application(environ, start_response):
    #print(urllib.parse)
    print(urllib.parse.parse_qs(environ['QUERY_STRING']))
    start_response('200 OK', [('Content-Type', 'application/json')])
    return forecast.main().encode('utf-8')
