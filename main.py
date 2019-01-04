import json
from datetime import datetime, timedelta, timezone
import tzlocal

# Self Imports
import forecast as weatherForcast

####################
# Constants
####################

forecast = weatherForcast.forecast()
    
with open('forecast.json', 'w') as outfile:
    del(forecast['hourly'])
    json.dump(forecast, outfile, indent=4)