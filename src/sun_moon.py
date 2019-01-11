from skyfield.toposlib import Topos
from skyfield.api import Loader
import skyfield.almanac as almanac
from skyfield.elementslib import osculating_elements_of
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

def moon_info(lat, lng, time=None):
    if (time == None):
        time = ts.now().astimezone(pytz.utc)
    else:
        time = datetime.fromtimestamp(time).astimezone(pytz.utc)
    time = ts.utc(time)

    moon = planets['moon']
    loc = earth + Topos(latitude_degrees=lat, longitude_degrees=lng)
    moon_loc = loc.at(time).observe(moon).apparent()
    moon_alt, _, _ = moon_loc.altaz()

    frac = almanac.fraction_illuminated(planets, 'moon', time)
    return {
        'pos': moon_alt.degrees,
        'above_horizon': bool(moon_alt.degrees > 0),
        'frac': frac
    }


def sun_info(lat, lng, timestamp=None):
    if (timestamp == None):
        timestamp = datetime.now().timestamp()
        # time = ts.now().astimezone(pytz.utc)

    time = datetime.fromtimestamp(timestamp).astimezone(pytz.utc)
    # time2 = datetime.fromtimestamp(timestamp + 500000).astimezone(pytz.utc)
    time = ts.utc(time)
    # time2 = ts.utc(time2)

    sun = planets['sun']
    earth_loc = Topos(latitude_degrees=lat, longitude_degrees=lng)
    loc = earth + earth_loc
    # t, y = almanac.find_discrete(time, time2, body_above_angle(planets, 'sun', -18, earth_loc))
    # print([x.utc_datetime().isoformat() for x in t], y)

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
