import forecast
import pylunar
from datetime import datetime
####################
# Constants
GLENS_FALLS_LAT = (43, 30, 95)
GLENS_FALLS_LONG = (-73, 64, 40)
####################

Moon = pylunar.MoonInfo(GLENS_FALLS_LAT, GLENS_FALLS_LONG)

# print(datetime(datetime.year, datetime.month, datetime.day))
# Moon.update()
# print(Moon.age())

# print(forecast.forecast())
