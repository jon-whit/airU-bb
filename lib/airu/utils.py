import threading
from gps import *

class GpsPoller(threading.Thread):

    def __init__(self):
        """
        Constructs a new GpsPoller object.

        A GpsPoller is invoked on a separate thread and runs continuously
        until the thread is terminated. The GpsPoller should be used to
        get the latest GPS data at any given time.
        """

        threading.Thread.__init__(self)
        self.session = gps(mode=WATCH_ENABLE)
        self.current_value = None
        self.running = True

    def get_gps_data(self):
        """
        Gets the latest GPS data from the GPS client.

        :return: A dictionary of fixtures from the GPS client.
        """
        return self.current_value

    def run(self):
        """
        Overrides the Thread's 'run' method. This method is invoked when the
        thread begins, and it continues to run until this GpsPoller's 'running'
        field is set to False.
        """
        while self.running:
            self.current_value = self.session.next()


def get_mac(interface):
    """
    Gets the MAC address for the supplied interface or None if the MAC could
    not be read from the system.

    :param interface: The network interface whose MAC should be returned
    :return: The unique MAC address, or None otherwise.
    """

    try:
        result = open('/sys/class/net/{0}/address'.format(interface)).readline()[0:17]
    except IOError:
        result = None

    return result
