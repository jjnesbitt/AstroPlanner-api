from skyfield.toposlib import Topos
from skyfield.api import Loader
import skyfield.almanac as almanac
from skyfield.elementslib import osculating_elements_of
from datetime import datetime
import pytz
import json

load = Loader('../data/skyfield')
ts = load.timescale()
planets = load('./de421.bsp')

earth = planets['earth']

DAY_S = 86400

'''
lat, lng should be float values
time should be a unix timestamp
'''


def body_above_angle(ephemeris, body, angle, topos):
    """Build a function of time that returns whether the specified body is above the desired angle.

    The function that this returns will expect a single argument that is
    a :class:`~skyfield.timelib.Time` and will return ``True`` if the
    sun is up, else ``False``.

    """
    body_to_observe = ephemeris[body]
    topos_at = (earth + topos).at

    def is_body_up_at(t):
        """Return `True` if the body has risen by time `t`."""
        # t._nutation_angles = iau2000b(t.tt)
        return topos_at(t).observe(body_to_observe).apparent().altaz()[0].degrees > angle

    is_body_up_at.rough_period = 0.5  # twice a day
    return is_body_up_at


def moon_illuminated(time):
    return almanac.fraction_illuminated(planets, 'moon', ts.utc(datetime.fromtimestamp(time).astimezone(pytz.utc)))

def moon_info(lat, lng, tz, startTime, endTime=None, ANGLE_THRESHOLD=-0.8333):
    """Returns information about the moon, between the start and end time. 
    If endTime is not specified, the passed startTime will be treated as the start of
    the day, and the end time will be 24 hours after the startTime. Start and End times 
    should be unix timestamps.
    
    The functions returns an array of rise and set times, relative to the moon rise and set.
    """

    if (endTime == None):
        endTime = startTime + DAY_S

    time = ts.utc(datetime.fromtimestamp(startTime).astimezone(tz))
    time2 = ts.utc(datetime.fromtimestamp(endTime).astimezone(tz))
    earth_loc = Topos(latitude_degrees=lat, longitude_degrees=lng)
    t, y = almanac.find_discrete(time, time2, body_above_angle(planets, 'moon', ANGLE_THRESHOLD, earth_loc), epsilon=(1/DAY_S), num=6)

    times_dict = {}
    for i, v in enumerate(t):
        dt = v.utc_datetime()
        dt_str = dt.date().isoformat()

        if (dt_str not in times_dict):
            times_dict[dt_str] = {}
        
        key = 'rise' if y[i] == True else 'set'
        times_dict[dt_str][key] = int(dt.timestamp())
    
    return times_dict


def sun_info(lat, lng, tz, startTime, endTime=None, ANGLE_THRESHOLD=-18.0):
    """Returns information about the sun, between the start and end time. 
    If endTime is not specified, the passed startTime will be treated as the start of
    the day, and the end time will be 24 hours after the startTime. Start and End times 
    should be unix timestamps.
    
    The functions returns an array of rise and set times, relative to the astronomical twilight.
    """
    
    if (endTime == None):
        endTime = startTime + DAY_S

    time = ts.utc(datetime.fromtimestamp(startTime).astimezone(tz))
    time2 = ts.utc(datetime.fromtimestamp(endTime).astimezone(tz))
    earth_loc = Topos(latitude_degrees=lat, longitude_degrees=lng)
    t, y = almanac.find_discrete(time, time2, body_above_angle(planets, 'sun', ANGLE_THRESHOLD, earth_loc), epsilon=(1/DAY_S), num=6)

    times_dict = {}
    for i, v in enumerate(t):
        dt = v.utc_datetime()
        dt_str = dt.date().isoformat()

        if (dt_str not in times_dict):
            times_dict[dt_str] = {}
        
        key = 'rise' if y[i] == True else 'set'
        times_dict[dt_str][key] = int(dt.timestamp())

    return times_dict


def sun_moon_info(lat, lng, tz, startTime, endTime=None):
    info = {}
    info['sun'] = sun_info(lat, lng, tz, startTime, endTime)
    info['moon'] = moon_info(lat, lng, tz, startTime, endTime)

    return info
