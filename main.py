import json
from datetime import datetime, timedelta, timezone
import tzlocal

# Self Imports
import forecast as weatherForcast


####################
# Constants
####################

forecast = weatherForcast.forecast()

# with open('forecast.json', 'w') as outfile:
#     json.dump(forecast, outfile, indent=4)

forecastDays = forecast['daily']['data']
# moonInfo = [weatherForcast.moonInfo(time=x['time']) for x in forecastDays]

for x in forecastDays:
    x['moonInfo'] = weatherForcast.moonInfo(time=x['time'])

print(forecastDays)
with open('forecast.json', 'w') as outfile:
    json.dump(forecastDays, outfile, indent=4)

# print([x['rise'].ctime() for x in moonInfo])
# print([x['set'].ctime() for x in moonInfo])