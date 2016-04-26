from process import Process
import re

class MacAddress():
  def __init__(self):
    self.addr = self.get_mac()

  def get_mac(self):
    """
    Obtains the device's MACAddress from "ifconfig".
    :return: The device's MACAddress
    """
    regex = r'(HWaddr\s{1}..:..:..:..:..:..)'

    ps = Process(['/sbin/ifconfig', 'eth0'])
    ps.run()
    
    if re.search(regex, ps.output()):
      match = re.search(regex, ps.output())
      HWaddr = match.group(0).split(' ')
      return HWaddr[1]
