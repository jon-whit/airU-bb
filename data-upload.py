import json
import requests
from lib.airu.dbmodels import *
from lib.airu.utils import get_mac

def prepare_db():
  """
  Establishes a connection with the database.
  """
  # remove '/root/' when testing with mock_data
  db.init('/root/air-metrics.db')
  db.connect()

def fetch_data():
  """
  Queries local database for all metrics which have not been uploaded to AirU server.

  :return: An array of all data metrics which have not been uploaded.
  """
  return AirMeasurement().select().where(~(AirMeasurement.uploaded))

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
      "Station": { "Id": get_mac('eth0') },
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

if __name__ == '__main__':
  """
  Entry point for uploaded Beaglebone data to server API.
  """
  prepare_db()
  metrics = fetch_data()
  if len(metrics) > 0:
    # only upload if there is something to upload
    upload(encode_data(metrics), metrics)
