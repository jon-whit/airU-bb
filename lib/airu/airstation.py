import time
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_DHT
import utils
from exception import InitException

# Define constants specific to an AirStation (pin numbers, etc..)
DHT22_PIN = 4

class AirStation:
    """
    Represents an airU AirStation.

    An airU AirStation object is used to collect the various data readings from the sensors
    connected to the station.
    """

    def __init__(self):
        """
        Constructs an AirStation object.
        """

        if not self._init_station():
            raise InitException("Could not initialize the AirStation!")

    def __enter__(self):
        return self

    def _init_station(self):
        """
        Attempts to initialize this AirStation object.

        This method is used to initialize the various fields and sensors of an AirStation object.
        If the object cannot be initialized then this method returns False, otherwise it returns
        True.

        :return: True if the AirStation could be initialized. False otherwise.
        """
        self._id = utils.get_mac('eth0')
        self._bmp = BMP085.BMP085()
        self._gpsp = utils.GpsPoller()
        self._gpsp.start()  # start polling the GPS sensor

        # Wait a few seconds to ensure a GPS fix
        time.sleep(5)
        location = self.get_location()
        self._lat = location[0]
        self._lon = location[1]

        return True

    def get_id(self):
        """
        Gets the unique ID for this AirStation.

        An AirStation object is identified by its unique 64-bit MAC address of the
        network card that it is using.

        :return: A MAC address as a string, or None if the MAC could not be read.
        """

        return self._id

    def get_location(self):
        """
        Gets the latitudinal and longitudinal coordinates of this AirStation as a tuple.

        :return: A tuple containing the latitude and longitude, respectively.
        """

        gps_data = self._gpsp.get_gps_data()
        return gps_data['lon'], gps_data['lat']

    def get_temp(self, retries=5):
        """
        Gets the current temperature as reported by the BMP085/BMP180 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from Bosch.

        https://ae-bst.resource.bosch.com/media/products/dokumente/bmp180/BST-BMP180-DS000-12~1.pdf

        :param retries: The number of times to retry to get a reading (default 5)
        :return: A float representing the current temperature, or None if no reading was obtained in the retry period.
        """

        # todo: improve this definition so that it returns None if a result is not returned
        # within after some number of retries
        return self._bmp.read_temperature()

    def get_pressure(self, retries=5):
        """
        Gets the current pressure as reported by the BMP085/BMP180 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from Bosch.

        https://ae-bst.resource.bosch.com/media/products/dokumente/bmp180/BST-BMP180-DS000-12~1.pdf

        :param retries: The number of times to retry to get a reading (default 5)
        :return: A float representing the current barometric pressure, or None if no reading was obtained in the retry
                 period.
        """

        # todo: improve this definition so that it returns None if a result is not returned
        # within after some number of retries
        return self._bmp.read_pressure()

    def get_altitude(self, retries=5):
        """
        Gets the current altitude as reported by the BMP085/BMP180 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from Bosch.

        https://ae-bst.resource.bosch.com/media/products/dokumente/bmp180/BST-BMP180-DS000-12~1.pdf

        :param retries: The number of times to retry to get a reading (default 5)
        :return: A float representing the current altitude, or None if no reading was obtained in the retry period.
        """

        # todo: improve this definition so that it returns None if a result is not returned
        # within after some number of retries
        return self._bmp.read_altitude()

    def get_humidity(self, retries=15):
        """
        Gets the current percentage of humidity as reported by the DHT11/DHT22 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from AOSONG.

        http://akizukidenshi.com/download/ds/aosong/AM2302.pdf

        :param retries: The number of times to retry to get a reading (default 15)
        :return: A float representing the percentage of humidity, or None if no reading was obtained in the retry
                 period.
        """

        # todo: improve this definition so that it returns None if a result is not returned
        # within after some number of retries
        return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_PIN, retries=retries)[0]

    def close(self):
        """
        Closes all of the open resources for this AirStation.

        This method should be invoked at the end of life for each AirStation
        object.
        """

        # Stop the GpsPoller in the extra thread
        self._gpsp.running = False
        self._gpsp.join()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager  method which is invoked on exit from the body of a
        with statement.

        See: https://www.python.org/dev/peps/pep-0343/
        """
        self.close()
