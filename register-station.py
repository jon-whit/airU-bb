from lib.airu.macaddress import MacAddress
import requests
import pprint

if __name__ == '__main__':
  """
  Uploads the MACAddress to the server for station registration.
  """
  mac = MacAddress()

  # TODO: remove 'dev' from URL when API is re-deployed to PROD
  # TODO: replace ???*??? with endpoint once it is implemented
  url     = 'http://dev.air.eng.utah.edu/api/stations/???waiting_for_endpoint???'
  headers = {'Content-Type': 'application/json'}
  message = {"DeviceID": mac.addr}

  r = requests.post(url, data=json.dumps(message), headers=headers)
  if r.status_code == 200:
    print 'Device Registered.'
  else:
    print 'A server error occurred.'