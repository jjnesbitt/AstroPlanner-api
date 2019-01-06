import json
from datetime import datetime, timedelta, timezone
import tzlocal

# Self Imports
import forecast as weatherForcast

####################
# Constants
FORECAST_FILE = '../data/forecast.json'
####################

def main(params):
    if ('lat' not in params or 'lng' not in params):
        return json.dumps({'status': "Error", 'message': "Not enough parameters included"}, indent=4)

    forecast = weatherForcast.forecast(lat=params['lat'], lng=params['lng'])
    del(forecast['hourly'])

    with open(FORECAST_FILE, 'w') as outfile:
        json.dump(forecast, outfile, indent=4)

    return json.dumps(forecast, indent=4)


if __name__ == '__main__':
    main()
