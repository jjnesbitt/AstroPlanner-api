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
        return None


def get_sunrise_sunset_info(currentTime=datetime.now(), lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    res = None
    params = {'lat': lat, 'lng': lng,
              'date': currentTime.date().isoformat(), 'formatted': 0}
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


def get_moon_info(currentTime=datetime.now().timestamp(), tz='US/Eastern', lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
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

    currentTime = datetime.fromtimestamp(currentTime)
    timezone = pytz.timezone(tz)
    Moon = pylunar.MoonInfo(lat_tuple, lng_tuple)
    Moon.update(currentTime.utctimetuple()[:6])

    rise_set_times = Moon.rise_set_times(tz)
    fractional_phase = Moon.fractional_phase()

    info = {}
    for k, v in rise_set_times:
        if type(v) == str:
            top = datetime.combine(
                currentTime.date(), time(0, 0, 0)).timestamp()
            if k == 'rise':
                info[k] = top
            elif k == 'set':
                info[k] = top + ONE_DAY_SECONDS
        else:
            info[k] = datetime(*v, 0, timezone).timestamp()

    info['frac'] = fractional_phase
    return info


def forecast(lat=GLENS_FALLS_LAT, lng=GLENS_FALLS_LONG):
    status = 'OK'
    error = None

    res = raw_forecast(lat, lng)
    if (res == None):
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
        currentTime = datetime.fromtimestamp(day['sunriseTime']).astimezone(pytz.timezone(res['timezone']))
        # currentTime = datetime.fromtimestamp(day['time'])
        currentDateStr = str(currentTime.date())

        # day['moon_info'] = get_moon_info(
        #     currentTime=day['sunriseTime'], tz=res['timezone'])
        
        moon_info[currentDateStr] = get_moon_info(
            currentTime=day['sunriseTime'], tz=res['timezone'])

        sun_times[currentDateStr] = get_sunrise_sunset_info(
            currentTime=currentTime)

        # current_sun_times = sun_times[currentDateStr]
        
        # day['hours'] = list(filter(lambda x: x['time'] >= day['time']
        #                            and x['time'] < day['time'] + ONE_DAY_SECONDS, res['hourly']['data']))

        # for hour in day['hours']:
        #     hour['dark'] = (hour['time'] < current_sun_times['astronomical_twilight_begin']
        #                     or hour['time'] > current_sun_times['astronomical_twilight_end'])

        #     hour['moonVisible'] = (hour['time'] >= day['moon_info']['rise']
        #                            and hour['time'] <= day['moon_info']['set'])

        #     if (not hour['dark']):
        #         hour['viability'] = 0
        #     else:
        #         hour['viability'] = 1 - (hour['cloudCover']
        #                                  + day['moon_info']['frac'])/2 if hour['moonVisible'] else 1 - hour['cloudCover']

    # print(json.dumps(sun_times, indent=4))
    for hour in res['hourly']['data']:
        currentTime = datetime.fromtimestamp(hour['time'])
        # top = datetime.combine(currentTime.date(), time(0, 0, 0)).timestamp()
        currentDayStr = str(currentTime.date())
        currentMoonInfo = moon_info[currentDayStr]

        hour['dark'] = (hour['time'] < sun_times[currentDayStr]['astronomical_twilight_begin']
            or hour['time'] > sun_times[currentDayStr]['astronomical_twilight_end'])
        
        hour['moonVisible'] = (hour['time'] >= currentMoonInfo['rise']
                        and hour['time'] <= currentMoonInfo['set'])
        
        if (not hour['dark']):
                hour['viability'] = 0
        else:
            hour['viability'] = 1 - (hour['cloudCover']
                + currentMoonInfo['frac'])/2 if hour['moonVisible'] else 1 - hour['cloudCover']


    res['status'] = status
    return res
