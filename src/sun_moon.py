from skyfield.toposlib import Topos
from skyfield.api import Loader
from skyfield.almanac import fraction_illuminated
from datetime import datetime
import pytz

load = Loader('../data/skyfield')
ts = load.timescale()
planets = load('./de421.bsp')

earth = planets['earth']


'''
lat, lng should be float values
time should be a unix timestamp
'''


def moon_info(lat, lng, time=None):
    if (time == None):
        time = ts.now().astimezone(pytz.utc)
    else:
        time = datetime.fromtimestamp(time).astimezone(pytz.utc)
    time = ts.utc(time)

    moon = planets['moon']
    loc = earth + Topos(latitude=lat, longitude=lng)
    moon_loc = loc.at(time).observe(moon).apparent()
    moon_alt, _, _ = moon_loc.altaz()

    frac = fraction_illuminated(planets, 'moon', time)
    return {
        'pos': moon_alt.degrees,
        'above_horizon': moon_alt.degrees > 0,
        'frac': frac
    }


def sun_info(lat, lng, time=None):
    if (time == None):
        time = ts.now().astimezone(pytz.utc)
    else:
        time = datetime.fromtimestamp(time).astimezone(pytz.utc)
    time = ts.utc(time)

    sun = planets['sun']
    loc = earth + Topos(latitude=lat, longitude=lng)
    sun_loc = loc.at(time).observe(sun).apparent()
    sun_alt, _, _ = sun_loc.altaz()

    return {
        'pos': sun_alt.degrees,
        'above_astro_twilight': sun_alt.degrees > -18
    }


def sun_moon_info(lat, lng, time=None):
    info = {}
    info['sun'] = sun_info(lat, lng, time)
    info['moon'] = moon_info(lat, lng, time)

    return info
