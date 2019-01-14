import json
import requests
import pylunar
import tzlocal
import pytz
from datetime import datetime, time
from dateutil import parser
from credentials import DARK_SKY_SECRET
from sun_moon import sun_moon_info, moon_illuminated

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

    moon_phases = {}
    for day in res['daily']['data']:
        date = datetime.fromtimestamp(day['time']).astimezone(pytz.timezone(res['timezone'])).date()
        moon_phases[date.isoformat()] = moon_illuminated(day['time'])

    startTime = res['daily']['data'][0]['time']
    endTime = res['daily']['data'][len(res['daily']['data']) - 1]['time'] + DAY_S
    sun_moon_times = sun_moon_info(lat, lng, pytz.timezone(res['timezone']), startTime=startTime, endTime=endTime)

    for hour in res['hourly']['data']:
        dt = datetime.fromtimestamp(hour['time']).astimezone(pytz.timezone(res['timezone']))
        date_str = dt.date().isoformat()

        hour['dark'] = (hour['time'] < sun_moon_times['sun'][date_str]['rise'] or hour['time'] > sun_moon_times['sun'][date_str]['set'])

        if ('rise' not in sun_moon_times['moon'][date_str]):
            hour['moonVisible'] = (hour['time'] < sun_moon_times['moon'][date_str]['set'])
        elif ('set' not in sun_moon_times['moon'][date_str]):
            hour['moonVisible'] = (hour['time'] > sun_moon_times['moon'][date_str]['rise'])
        else:
            if (sun_moon_times['moon'][date_str]['set'] < sun_moon_times['moon'][date_str]['rise']):
                hour['moonVisible'] = (hour['time'] < sun_moon_times['moon'][date_str]['rise'] or hour['time'] > sun_moon_times['moon'][date_str]['set'])
            else:
                hour['moonVisible'] = (hour['time'] > sun_moon_times['moon'][date_str]['rise'] and hour['time'] < sun_moon_times['moon'][date_str]['set'])

        if (not hour['dark']):
            hour['viability'] = 0
        else:
            hour['viability'] = 1 - (hour['cloudCover']
                + moon_phases[date_str])/2 if hour['moonVisible'] else 1 - hour['cloudCover']

    res['status'] = status
    return res
