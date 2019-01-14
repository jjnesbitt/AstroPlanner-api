# Random code goes here, not always for testing


import forecast
import sun_moon
import json
import pytz
from datetime import datetime
import time
import main

GLENS_FALLS_LAT = 43.3095
GLENS_FALLS_LONG = -73.6440

TEST_LAT = 29.9479
TEST_LONG = -85.4179

start = time.time()
res = forecast.forecast(lat=TEST_LAT, lng=TEST_LONG)
end = time.time()
print("runtime of forecast", end - start)

# start = time.time()
# res = forecast.dark_sky_forecast(lat=12.4444, lng=21.3333)
# end = time.time()
# print("runtime of dark_sky_forecast", end - start)

start = time.time()
res = sun_moon.sun_moon_info(GLENS_FALLS_LAT, GLENS_FALLS_LONG, pytz.timezone('America/New_York'), startTime=datetime.now().timestamp(), endTime=datetime.now().timestamp() + 86400*7)
moon_frac = sun_moon.moon_illuminated(datetime.now().timestamp())
end = time.time()
# print(json.dumps(res, indent=4))
print("runtime of sun_moon_info", end - start)

start = time.time()
res = sun_moon.moon_illuminated(datetime.now().timestamp())
end = time.time()
print("runtime of moon_illuminated", end - start)

#print(json.dumps(res, indent=4))
