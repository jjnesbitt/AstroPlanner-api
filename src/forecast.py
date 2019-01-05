import requests
import json
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
        print("Error retrieving forcast")
        return None


def get_sunrise_sunset_info(time=datetime.now(), lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    res = None
    params = {'lat': lat, 'lng': lng, 'date': time.isoformat(), 'formatted': 0}
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


def moon_info(time=datetime.now().timestamp(), tz='US/Eastern', lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
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

    time = datetime.fromtimestamp(time)
    Moon = pylunar.MoonInfo(lat_tuple, lng_tuple)
    Moon.update(time.utctimetuple()[:6])

    rise_set_times = Moon.rise_set_times(tz)
    fractional_phase = Moon.fractional_phase()

    info = {x[0]: datetime(*x[1], 0, tzlocal.get_localzone()).timestamp()
            for x in rise_set_times}
    info['frac'] = fractional_phase
    return info


def forecast(lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    res = raw_forecast(lat, lng)
    if (res == None):
        return None

    times_updated = False
    try:
        sun_times = json.load(open(SUNRISE_SUNSET_FILE, 'r'))
    except:
        sun_times = {}

    for day in res['daily']['data']:
        currentDay = datetime.fromtimestamp(day['sunriseTime'])
        currentDateStr = str(currentDay.date())

        day['moon_info'] = moon_info(
            time=day['sunriseTime'], tz=res['timezone'])

        if currentDateStr not in sun_times:
            print("NEW SUNRISE API CALL")
            times_updated = True
            sun_times[currentDateStr] = get_sunrise_sunset_info(
                time=currentDay)

        current_sun_times = sun_times[currentDateStr]
        day['hours'] = list(filter(lambda x: x['time'] >= day['time']
                                   and x['time'] < day['time'] + ONE_DAY_SECONDS, res['hourly']['data']))

        for hour in day['hours']:
            hour['dark'] = (hour['time'] < current_sun_times['astronomical_twilight_begin']
                            or hour['time'] > current_sun_times['astronomical_twilight_end'])

            hour['moonVisible'] = (hour['time'] >= day['moon_info']['rise']
                and hour['time'] <= day['moon_info']['set'])

            if (not hour['dark']):
                hour['viability'] = 0
            else:
                hour['viability'] = 1 - (hour['cloudCover']
                    + day['moon_info']['frac'])/2 if hour['moonVisible'] else 1 - hour['cloudCover']

    if (times_updated):
        print("NEW WRITE")
        json.dump(sun_times, open(SUNRISE_SUNSET_FILE, 'w'), indent=4)

    return res
