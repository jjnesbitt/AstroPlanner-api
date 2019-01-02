import forecast as weatherForcast
import pylunar
import json
from datetime import datetime, timedelta, timezone

####################
# Constants
####################

forecast = weatherForcast.forecast()



with open('forecast.json', 'w') as outfile:
    json.dump(forecast, outfile, indent=4)