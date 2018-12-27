import requests
import json
from datetime import datetime
from dateutil import parser

#######################

r = requests.get('https://api.weather.gov/gridpoints/ALY/58,90/forecast')
res = json.loads(r.text)
periods = res['properties']['periods']

nightPeriods = list(filter(lambda x: x['isDaytime'] == False, periods))

for item in nightPeriods:
    item['date'] = parser.parse(item['startTime'])

