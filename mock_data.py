import json
import requests
from lib.airu.dbmodels import *
import datetime
import math
import random
import pprint

if __name__ == '__main__':
  # use non-root level DB for testing
  db.init('air-metrics.db')
  db.connect()
  db.create_tables([AirMeasurement], True)

  lat = 40.687033
  lon = -111.824517
  altitude = 1432

  time = datetime.datetime.now()
  date = datetime.timedelta(seconds=3155690)
  time = time - date

  for i in range(1, 1428):
    date = datetime.timedelta(seconds=9000)
    time = time + date

    pm1  = abs(math.sin(i) + random.uniform(0.1,23))
    pm25 = abs(math.cos(i) + random.uniform(0.1, 17))
    pm10 = abs(math.asinh(i) + random.uniform(0.1, 32))
    temp = abs(math.sin(i) + random.uniform(0.1, 1))
    humidity = abs(math.asinh(i) + random.uniform(0.1, 1))
    pressure = abs(math.sin(i) + random.uniform(0.1, 1))

    measurement = AirMeasurement(type='Temperature', value=temp, unit='C', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Humidity', value=humidity, unit='%', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Pressure', value=pressure, unit='Pascal', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Altitude', value=altitude, unit='M', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='PM1.0', value=pm1, unit='UG/M3', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='PM2.5', value=pm25, unit='UG/M3', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='PM10', value=pm10, unit='UG/M3', latitude=lat, longitude=lon)
    measurement.save()
