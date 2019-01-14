import json
import requests
import pylunar
import tzlocal
import pytz
from datetime import datetime, time
from dateutil import parser
from credentials import DARK_SKY_SECRET
from sun_moon import sun_moon_info

#######################
# Constants
GLENS_FALLS_LAT = 43.3095
GLENS_FALLS_LONG = -73.6440

DARK_SKY_API_PATH = 'https://api.darksky.net/forecast/' + DARK_SKY_SECRET

SUNRISE_SUNSET_BASE_PATH = 'https://api.sunrise-sunset.org/json'
SUNRISE_SUNSET_FILE = '../data/sun_times.json'
DAY_S = 86400
#######################


def dark_sky_forecast(lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    res = None
    params = {'extend': 'hourly', 'exclude': ['minutely']}
    headers = {'content-encoding': 'gzip'}

    path = '/' + str(lat) + ',' + str(lng)
    try:
        res = requests.get(DARK_SKY_API_PATH + path,
                           params=params, headers=headers)
        return json.loads(res.text)
    except:
        return None


def forecast(lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    status = 'OK'
    error = None

    res = dark_sky_forecast(lat, lng)
    if (res is None):
        status = 'Error'
        error = "Error Retrieving Forecast"

    elif ('error' in res):
        status = 'Error'
        error = res['error']

    ###

    if (error != None):
        return {'status': status, 'error': error}

    for day in res['daily']['data']:
        #Do something with moon calls
        continue
    
    startTime = res['daily']['data'][0]['time']
    endTime = res['daily']['data'][len(res['hourly']['data']) - 1]['time'] + DAY_S

    sun_moon_times = sun_moon_info(lat, lng, startTime=startTime, endTime=endTime)
    return res

    for hour in res['hourly']['data']:
        # current_sun_moon_info = sun_moon_info(lat, lng, hour['time'])

        # hour['dark'] = not current_sun_moon_info['sun']['above_astro_twilight']
        hour['dark'] = not current_sun_moon_info['sun']['above_astro_twilight']
        # hour['moonVisible'] = current_sun_moon_info['moon']['above_horizon']
        hour['moonVisible'] = current_sun_moon_info['moon']['above_horizon']

        if (not hour['dark']):
            hour['viability'] = 0
        else:
            hour['viability'] = 1 - (hour['cloudCover']
                + current_sun_moon_info['moon']['frac'])/2 if hour['moonVisible'] else 1 - hour['cloudCover']

    res['status'] = status
    return res
