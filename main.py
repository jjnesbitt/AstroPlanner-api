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

        if (not hour['dark']):
            hour['viability'] = 0
        else:
            hour['viability'] = 1 - (hour['cloudCover'] + day['moonPhase'])/2 if hour['moonVisible'] else 1 - hour['cloudCover']
    
    # print(len(day['hours']))
    
with open('forecast.json', 'w') as outfile:
    del(forecast['hourly'])
    json.dump(forecast, outfile, indent=4)