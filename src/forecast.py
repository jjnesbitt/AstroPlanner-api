import json
import requests
import pylunar
import tzlocal
import pytz
from datetime import datetime, time
from dateutil import parser
from credentials import DARK_SKY_SECRET

#######################
# Constants
GLENS_FALLS_LAT = 43.3095
GLENS_FALLS_LONG = -73.6440

DARK_SKY_API_PATH = 'https://api.darksky.net/forecast/' + DARK_SKY_SECRET

SUNRISE_SUNSET_BASE_PATH = 'https://api.sunrise-sunset.org/json'
SUNRISE_SUNSET_FILE = '../data/sun_times.json'
ONE_DAY_SECONDS = 86400
#######################


def raw_forecast(lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
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


def get_sunrise_sunset_info(current_time=datetime.now(), lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    res = None
    params = {'lat': lat, 'lng': lng,
              'date': current_time.date().isoformat(), 'formatted': 0}
    error = False

    try:
        res = requests.get(SUNRISE_SUNSET_BASE_PATH, params=params)
    except:
        error = True

    res = json.loads(res.text)

    if (error or res['status'] != 'OK'):
        print("Error retrieving forcast")
        return None

    res = res['results']
    res = {k: parser.parse(v).timestamp()
           for k, v in res.items() if k != 'day_length'}
    return res


def get_moon_info(current_time=datetime.now().timestamp(), tz='US/Eastern', lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    lat_string_pair = "{:.4f}".format(lat).split('.')
    lng_string_pair = "{:.4f}".format(lng).split('.')

    lat_tuple = (
        int(lat_string_pair[0]),
        int(lat_string_pair[1][:2]),
        int(lat_string_pair[1][2:])
    )
    lng_tuple = (
        int(lng_string_pair[0]),
        int(lng_string_pair[1][:2]),
        int(lng_string_pair[1][2:])
    )

    current_time = datetime.fromtimestamp(current_time)
    Moon = pylunar.MoonInfo(lat_tuple, lng_tuple)
    Moon.update(current_time.utctimetuple()[:6])

    rise_set_times = Moon.rise_set_times(tz)

    info = {}
    for k, v in rise_set_times:
        if isinstance(v, str):
            top = datetime.combine(
                current_time.date(), time(0, 0, 0)).timestamp()
            if k == 'rise':
                info[k] = top
            elif k == 'set':
                info[k] = top + ONE_DAY_SECONDS
        else:
            info[k] = datetime(*v, 0, pytz.timezone(tz)).timestamp()

    info['frac'] = Moon.fractional_phase()
    return info


def forecast(lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    status = 'OK'
    error = None

    res = raw_forecast(lat, lng)
    if (res is None):
        status = 'Error'
        error = "Error Retrieving Forecast"

    elif ('error' in res):
        status = 'Error'
        error = res['error']

    ###

    if (error != None):
        return {'status': status, 'error': error}

    sun_times = {}
    moon_info = {}
    for day in res['daily']['data']:
        current_time = datetime.fromtimestamp(
            day['sunriseTime']).astimezone(pytz.timezone(res['timezone']))
        current_date_str = str(current_time.date())

        moon_info[current_date_str] = get_moon_info(
            current_time=day['sunriseTime'], tz=res['timezone'])

        sun_times[current_date_str] = get_sunrise_sunset_info(
            current_time=current_time)

    for hour in res['hourly']['data']:
        current_time = datetime.fromtimestamp(hour['time'])
        current_date_str = str(current_time.date())
        current_moon_info = moon_info[current_date_str]

        hour['dark'] = (hour['time'] < sun_times[current_date_str]['astronomical_twilight_begin']
            or hour['time'] > sun_times[current_date_str]['astronomical_twilight_end'])

        hour['moonVisible'] = (hour['time'] >= current_moon_info['rise']
            and hour['time'] <= current_moon_info['set'])

        if (not hour['dark']):
            hour['viability'] = 0
        else:
            hour['viability'] = 1 - (hour['cloudCover']
                                     + current_moon_info['frac'])/2 if hour['moonVisible'] else 1 - hour['cloudCover']

    res['status'] = status
    return res
