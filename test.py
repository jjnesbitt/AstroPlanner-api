# Random code goes here, not actually for testing


import forecast
import json
import pytz
from datetime import datetime

times = forecast.get_sunrise_sunset_info()
if (times == None):
    exit()

print(json.dumps(times, indent=4))

