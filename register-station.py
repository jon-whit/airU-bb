import json
import requests
from lib.airu.utils import get_mac

if __name__ == '__main__':
  """
  Uploads the MACAddress to the server for station registration.
  """

  # TODO: remove 'dev' from URL when API is re-deployed to PROD
  # TODO: replace ???*??? with endpoint once it is implemented
  url     = 'http://dev.air.eng.utah.edu/api/stations/???waiting_for_endpoint???'
  headers = {'Content-Type': 'application/json'}
  message = {"DeviceID": get_mac('eth0')}

  r = requests.post(url, data=json.dumps(message), headers=headers)
  if r.status_code == 200:
    print 'Device Registered.'
  else:
    print 'A server error occurred.'
