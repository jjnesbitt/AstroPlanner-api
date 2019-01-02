import requests
import json
from dateutil import parser
from credentials import DARK_SKY_SECRET

#######################
# Constants
GLENS_FALLS_LAT = 43.3095
GLENS_FALLS_LONG = -73.6440
# BASE_API_PATH = 'https://api.weather.gov/gridpoints/'
# GLENS_FALLS_PATH = 'ALY/58,90/forecast'
BASE_API_PATH = 'https://api.darksky.net/forecast/' + DARK_SKY_SECRET
GLENS_FALLS_PATH = '/' + str(GLENS_FALLS_LAT) + ',' + str(GLENS_FALLS_LONG)
#######################


def raw_forecast(path=GLENS_FALLS_PATH):
    res = None
    try:
        res = requests.get(BASE_API_PATH + path)
        return json.loads(res.text)
    except:
        print("Error retrieving forcast")
        return None


def forecast(path=GLENS_FALLS_PATH):
    res = raw_forecast(path)

    if (res == None):
        return None

    # Do stuff
    # dailyTimes = [{k: v for k, v in x.items() if k in ['sunriseTime', 'sunsetTime', 'time']} for x in res['daily']['data']]
    for day in res['daily']['data']:
        darkHours = list(filter(lambda x: (x['time'] < day['sunriseTime'] or x['time'] > day['sunsetTime'])
            and x['time'] > day['time']
            and x['time'] < day['time'] + 86400, res['hourly']['data']))
        day['darkHours'] = darkHours

    # print(json.dumps(res['daily'], indent=4))
    return res

# forecast()
