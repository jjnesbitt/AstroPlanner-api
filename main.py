import json
from datetime import datetime, timedelta, timezone
import tzlocal

# Self Imports
import forecast as weatherForcast

####################
# Constants
####################

forecast = weatherForcast.forecast()
for day in forecast['daily']['data']:
    day['moonInfo'] = weatherForcast.moonInfo(time=day['sunriseTime'])
    
    for hour in day['hours']:
        hour['moonVisible'] = (hour['time'] >= day['moonInfo']['rise'] and hour['time'] <= day['moonInfo']['set'])
    
    # print(len(day['hours']))
    
with open('forecast.json', 'w') as outfile:
    json.dump(forecast, outfile, indent=4)