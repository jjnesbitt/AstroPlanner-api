from skyfield.toposlib import Topos
from skyfield.api import Loader
from datetime import datetime
import pytz 

GLENS_FALLS_LAT = 43.3095
GLENS_FALLS_LONG = -73.6440

load = Loader('../data/skyfield')
ts = load.timescale()
planets = load('./de421.bsp')

earth = planets['earth']


'''
lat, lng should be float values
time should be a unix timestamp
'''

def moon_pos(lat, lng, time=None):
    if (time == None):
        time = ts.now().astimezone(pytz.utc)
    else:
        time = datetime.fromtimestamp(time).astimezone(pytz.utc)
    time = ts.utc(time)

    moon = planets['moon']
    loc = earth + Topos(latitude=lat, longitude=lng)
    moon_loc = loc.at(time).observe(moon).apparent()
    moon_alt, _, _ = moon_loc.altaz()
    return moon_alt.degrees

def sun_pos(lat, lng, time=None):
    if (time == None):
        time = ts.now().astimezone(pytz.utc)
    else:
        time = datetime.fromtimestamp(time).astimezone(pytz.utc)
    time = ts.utc(time)

    sun = planets['sun']
    loc = earth + Topos(latitude=lat, longitude=lng)
    sun_loc = loc.at(time).observe(sun).apparent()
    sun_alt, _, _ = sun_loc.altaz()
    return sun_alt.degrees

def sun_moon_pos(lat, lng):
    result = {}
    result['sun'] = sun_pos(lat, lng)
    result['moon'] = moon_pos(lat, lng)

    return result