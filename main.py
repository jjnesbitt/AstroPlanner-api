import json
from datetime import datetime, timedelta, timezone
import tzlocal

# Self Imports
import forecast as weatherForcast

####################
# Constants
####################

forecast = weatherForcast.forecast()
forecastDays = forecast['daily']['data']
# moonInfo = [weatherForcast.moonInfo(time=x['time']) for x in forecastDays]

for day in forecastDays:
    day['moonInfo'] = weatherForcast.moonInfo(time=day['sunriseTime'])
    # day['darkHoursNoMoon'] = list(filter(lambda x: (x['time'] < day['moonInfo']['rise'] or x['time'] > day['moonInfo']['set']), day['darkHours']))
    
    for hour in day['darkHours']:
        hour['moonVisible'] = (hour['time'] >= day['moonInfo']['rise'] and hour['time'] <= day['moonInfo']['set'])
    
    print((len(day['darkHours']), len(day['darkHoursNoMoon'])))

# print(forecastDays)
with open('forecast.json', 'w') as outfile:
    json.dump(forecastDays, outfile, indent=4)