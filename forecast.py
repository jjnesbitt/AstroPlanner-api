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

DARK_SKY_API_PATH = 'https://api.darksky.net/forecast/' + DARK_SKY_SECRET
GLENS_FALLS_PATH = '/' + str(GLENS_FALLS_LAT) + ',' + str(GLENS_FALLS_LONG)

SUNRISE_SUNSET_BASE_PATH = 'https://api.sunrise-sunset.org/json'
#######################


def raw_forecast(path=GLENS_FALLS_PATH):
    res = None
    params = {'extend': 'hourly', 'exclude': ['minutely']}
    headers = {'content-encoding': 'gzip'}
    try:
        res = requests.get(DARK_SKY_API_PATH + path, params=params, headers=headers)
        return json.loads(res.text)
    except:
        print("Error retrieving forcast")
        return None


def get_sunrise_sunset_info(time=datetime.now(), lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    # NEED TO CONVERT RESPONSE TO LOCAL TIME

    res = None
    params = {'lat': lat, 'lng': lng, 'date': time.isoformat()}
    
    try:
        res = requests.get(SUNRISE_SUNSET_BASE_PATH, params=params)
        return json.loads(res.text)
    except:
        print("Error retrieving forcast")
        return None


def forecast(path=GLENS_FALLS_PATH):
    res = raw_forecast(path)

    if (res == None):
        return None

    for day in res['daily']['data']:
        day['hours'] = list(filter(lambda x: x['time'] > day['time'] and x['time'] < day['time'] + 86400, res['hourly']['data']))
        for hour in day['hours']:
            hour['dark'] = (hour['time'] < (day['sunriseTime'] - 10800) or hour['time'] > (day['sunsetTime'] + 10800))

    return res


def moonInfo(time=datetime.now().timestamp(), lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    lat_string_pair = "{:.4f}".format(lat).split('.')
    lng_string_pair = "{:.4f}".format(lng).split('.')

    lat_tuple = (int(lat_string_pair[0]), int(lat_string_pair[1][:2]), int(lat_string_pair[1][2:]))
    lng_tuple = (int(lng_string_pair[0]), int(lng_string_pair[1][:2]), int(lng_string_pair[1][2:]))

    time = datetime.fromtimestamp(time)
    Moon = pylunar.MoonInfo(lat_tuple, lng_tuple)
    Moon.update(time.utctimetuple()[:6])

    rise_set_times = Moon.rise_set_times('US/Eastern')
    return {x[0]: datetime(*x[1], 0, tzlocal.get_localzone()).timestamp() for x in rise_set_times}