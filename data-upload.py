#!/usr/bin/python
"""
data-upload.py

Author: Jonathan Whitaker
Email: jon.b.whitaker@gmail.com
Date: April 21, 2016

data-upload.py is an integral part of the AirU toolchain, serving as the script
which uploads the collected data from the AirU station. This script is designed 
to run using a Cron.
"""

def fetch_data(excludeNonPollutants):
  """
  Queries local database for all metrics which have not been uploaded to AirU server.

  :return: An array of all data metrics which have not been uploaded.
  """
  if excludeNonPollutants:
    return AirMeasurement().select().where(~AirMeasurement.uploaded,
                                          AirMeasurement.type != 'Temperature',
                                          AirMeasurement.type != 'Altitude',
                                          AirMeasurement.type != 'Pressure',
                                          AirMeasurement.type != 'Humidity',
                                          AirMeasurement.type != 'PM1.0').limit(500)

  return AirMeasurement().select().where(~(AirMeasurement.uploaded)).limit(500)

def encode_data(metrics):
  """
  Encodes an array of data metrics into a dictionary which can be used as JSON data.
  Below is the model expected by the server API.
    [{
        "Time": "12-31-2015",
        "Station": {
            "Id": "T1000"
        },
        "Parameter": {
            "Name": "PM2.5",
            "Unit": "UG/M3"
        },
        "Location": {
            "lat": 40.687033,
            "lng": -111.824517
        },
        "Value": 30
    }]
  """
  msg = []
  for m in metrics:
    msg.append({
      "Time": str(m.date_added),
      "Station": { "Id": get_mac('eth0').replace(':', '') },
      "Parameter": { "Name": m.type, "Unit": m.unit },
      "Location": { "lat": m.latitude, "lng": m.longitude },
      "Value": m.value
      })

  return msg

def upload(message, metrics):
  """
  Uploads JSON messages to AirU central server API.
  """
  
  url     = 'http://dev.air.eng.utah.edu/api/stations/data'
  headers = {'Content-Type': 'application/json'}

  print json.dumps(message)

  r = requests.post(url, data=json.dumps(message), headers=headers)
  print r.status_code # TODO: just printing for sanity check
  
  if r.status_code == 200:
    print 'OK! SUCCESS'
    for m in metrics:
      m.uploaded = True
      m.save()

  return r.status_code

if __name__ == '__main__':
  """
  Entry point for uploaded Beaglebone data to server API.
  """
  prepare_db()

  # server api has an unresolved bug which causes uploads to fail if the 
  # uploaded datapoint is a type without a computable AQI
  # sending non pollutants first, is a workaround until the bug is resolved
  pollutants = fetch_data(True)
  if len(pollutants) > 0:
    status_code = upload(encode_data(pollutants), pollutants)
    if status_code == 200:
      non_pollutants = fetch_data(False)
      upload(encode_data(non_pollutants), non_pollutants)
