import threading
from gps import *
from functools import wraps

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

def retry(e, retries=4, delay=1, logger=None):
    """
    A decorator that will retry whatever function that it decorates a specified
    number of times with a delay period between each try. If the decorated
    function does not return a result that is *not* None, then this decorator
    will raise the supplied exception.

    :param e: The exception to raise if the retry count is exceeded.
    :param retries: The of retries that should be carried out.
    :param delay: The time delay between retries (seconds).
    :param logger: An optional logger to use.
    """

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries = retries
            while mtries > 0:
                result = f(*args, **kwargs)

                if result is None:
                    time.sleep(delay)
                    mtries -= 1

                    if logger:
                        msg = "Call to '{0}' failed to acquire a value... Retrying in {1} seconds.".format(f.__name__,
                                                                                                           delay)
                        logger.warning(msg)
                else:
                    return result

            raise e("Call to '{0}' failed to acquire a value in the retry period.".format(f.__name__))

        return f_retry

    return deco_retry


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
