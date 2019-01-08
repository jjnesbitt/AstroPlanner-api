import json

# Self Imports
import forecast as weatherForcast

####################
# Constants
####################

def main(params):
    if ('lat' not in params or 'lng' not in params):
        return json.dumps({'status': "Error", 'error': "Not enough parameters included"}, indent=4)
    lat = params['lat'][0]
    lng = params['lng'][0]

    try:
        lat = float(lat)
        lng = float(lng)
    except ValueError:
        return json.dumps({'status': "Error", 'error': "Latitude and Longitude must be floats"}, indent=4)

    forecast = weatherForcast.forecast(lat=lat, lng=lng)
    if ('error' in forecast):
        return json.dumps(forecast, indent=4)

    # del(forecast['daily'])
    return json.dumps(forecast, indent=4)


# if __name__ == '__main__':
#     main()
