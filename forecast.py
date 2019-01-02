import requests
import json
import pylunar
import tzlocal
from datetime import datetime
from credentials import DARK_SKY_SECRET

#######################
# Constants
GLENS_FALLS_LAT = 43.3095
GLENS_FALLS_LONG = -73.6440
GLENS_FALLS_LAT_TUPLE = (43, 30, 95)
GLENS_FALLS_LONG_TUPLE = (-73, 64, 40)
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

    # dailyTimes = [{k: v for k, v in x.items() if k in ['sunriseTime', 'sunsetTime', 'time']} for x in res['daily']['data']]
    for day in res['daily']['data']:
        darkHours = list(filter(lambda x: (x['time'] < day['sunriseTime'] or x['time'] > day['sunsetTime'])
            and x['time'] > day['time']
            and x['time'] < day['time'] + 86400, res['hourly']['data']))
        day['darkHours'] = darkHours

    # print(json.dumps(res['daily'], indent=4))
    return res

def moonInfo(time=datetime.now().timestamp(), lat=GLENS_FALLS_LAT_TUPLE, long=GLENS_FALLS_LONG_TUPLE):
    time = datetime.fromtimestamp(time)
    Moon = pylunar.MoonInfo(lat, long)
    Moon.update(time.utctimetuple()[:6])
    
    rise_set_times = Moon.rise_set_times('US/Eastern')
    # return {x[0]: datetime(*x[1], 0, tzlocal.get_localzone()) for x in rise_set_times}
    return {x[0]: datetime(*x[1], 0, tzlocal.get_localzone()).timestamp() for x in rise_set_times}