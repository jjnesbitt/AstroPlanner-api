import urllib
import main as forecast

def application(environ, start_response):
    params = urllib.parse.parse_qs(environ['QUERY_STRING'])
    status = '200 OK'
    headers = [
        ('Content-Type', 'application/json'),
        ('Access-Control-Allow-Origin', 'localhost:3000'),
        ('Access-Control-Allow-Credentials', 'true'),
    ]

    start_response(status, headers)
    return forecast.main(params).encode('utf-8')
