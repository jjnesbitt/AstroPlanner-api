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

start = time.time()
res = forecast.forecast(lat=12.4444, lng=21.3333)
end = time.time()
print("runtime of forecast", end - start)

start = time.time()
res = forecast.raw_forecast(lat=12.4444, lng=21.3333)
end = time.time()
print("runtime of raw_forecast", end - start)

start = time.time()
res = sun_moon.sun_moon_info(lat=12.4444, lng=21.3333)
end = time.time()
print("runtime of sun_moon_info", end - start)


#print(json.dumps(res, indent=4))
