import requests
import json
from dateutil import parser

#######################
# Constants
BASE_API_PATH = 'https://api.weather.gov/gridpoints/'
GLENS_FALLS_PATH = 'ALY/58,90/forecast'
#######################


def raw_forecast(path=GLENS_FALLS_PATH):
    res = None
    try:
        res = requests.get(BASE_API_PATH + path)
        return res
    except:
        print("Error retrieving forcast")
        return None


def forecast(path=GLENS_FALLS_PATH):
    r = raw_forecast(path)

    if (r == None):
        return None

    res = json.loads(r.text)
    periods = res['properties']['periods']

    nightPeriods = list(filter(lambda x: x['isDaytime'] == False, periods))

    for item in nightPeriods:
        item['date'] = parser.parse(item['startTime'])

    return nightPeriods
