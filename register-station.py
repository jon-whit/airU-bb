import json
import requests
from lib.airu.utils import get_mac

if __name__ == '__main__':
  """
  Uploads the MACAddress to the server for station registration.
  """

  url     = 'http://dev.air.eng.utah.edu/api/stations/ping'
  headers = {'Content-Type': 'application/json'}
  message = {"id": get_mac('eth0').replace(':', '')}

  print message

  r = requests.post(url, data=json.dumps(message), headers=headers)
  if r.status_code == 200:
    print 'Device Registered.'
  else:
    print 'A server error occurred.'
