import json
from datetime import datetime, timedelta, timezone
import tzlocal

# Self Imports
import forecast as weatherForcast

####################
# Constants
FORECAST_FILE = '../data/forecast.json'
####################

def main():
    forecast = weatherForcast.forecast()
    del(forecast['hourly'])

    with open(FORECAST_FILE, 'w') as outfile:
        json.dump(forecast, outfile, indent=4)

    return json.dumps(forecast, indent=4)


if __name__ == '__main__':
    main()
