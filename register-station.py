#!/usr/bin/python
"""
register-station.py

Author: Jonathan Whitaker
Email: jon.b.whitaker@gmail.com
Date: April 21, 2016

register-station.py is a script which serves to send a registration call to the
AirU registration endpoint. This script is designed to run at station bootup. If
the station is already registered, the post conditions of this script will have
no effect.
"""
import requests
import json
from lib.airu.utils import get_mac

if __name__ == '__main__':
  """
  Uploads the MAC address to the server for station registration.
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
