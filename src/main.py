import json
from datetime import datetime, timedelta, timezone
import tzlocal

# Self Imports
import forecast as weatherForcast

####################
# Constants
FORECAST_FILE = './data/forecast.json'
####################

forecast = weatherForcast.forecast()
    
with open(FORECAST_FILE, 'w') as outfile:
    del(forecast['hourly'])
    json.dump(forecast, outfile, indent=4)