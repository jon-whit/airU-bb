import time
import Adafruit_DHT
import utils
import Adafruit_BBIO.ADC as ADC
from exception import RetryException
from exception import InitException
from utils import retry

# Define constants specific to an AirStation (pin numbers, etc..)
DHT22_PIN   = 'P8_11'
PM_PORT      = '/dev/ttyO1'
MODE_SWITCH = 'P8_7' 
CO_PIN      = 'AIN0'
NO2_PIN     = 'AIN1'
LAB_MODE    = 0
FIELD_MODE  = 1

class AirStation:
    """
    Represents an airU AirStation.

    An airU AirStation object is used to collect the various data readings from the sensors
    connected to the station.
    """

    def __init__(self, bmp, gpsp, pm, mode = FIELD_MODE):
        """
        Constructs an AirStation object.
        """

        self._id = utils.get_mac('eth0')
        self._mode = mode
        self._bmp = bmp
        self._gpsp = gpsp

        # Only field mode requires gelocation information
        if mode == FIELD_MODE:
          self._gpsp.start() # Start the GPS poller
        
        # Open a connection with the PMS3003 sensor
        self._pm = pm
        self._pm.close()
        self._pm.open()

        # Setup the ADC peripheral
        ADC.setup()

    def __enter__(self):
        return self

    def get_id(self):
        """
        Gets the unique ID for this AirStation.

        An AirStation object is identified by its unique 64-bit MAC address of the
        network card that it is using.

        :return: A MAC address as a string, or None if the MAC could not be read.
        """

        return self._id

    @retry(RetryException, retries=10)
    def get_location(self):
        """
        Gets the latitudinal and longitudinal coordinates of this AirStation as a tuple.

        :return: A tuple containing the latitude and longitude, respectively.
        """

        gps_data = self._gpsp.get_gps_data()
        
        if gps_data is not None:
            return gps_data['lon'], gps_data['lat']
        else:
            return None

    @retry(RetryException, retries=5)
    def get_temp(self):
        """
        Gets the current temperature as reported by the BMP085/BMP180 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from Bosch:

        https://ae-bst.resource.bosch.com/media/products/dokumente/bmp180/BST-BMP180-DS000-12~1.pdf

        :return: A float representing the current temperature.
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_PIN)[1]

    @retry(RetryException, retries=5)
    def get_pressure(self):
        """
        Gets the current pressure as reported by the BMP085/BMP180 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from Bosch:

        https://ae-bst.resource.bosch.com/media/products/dokumente/bmp180/BST-BMP180-DS000-12~1.pdf

        :return: A float representing the current barometric pressure.
        :raises: exception.RetryException if no reading was obtained in the retry period.

        """

        return self._bmp.read_pressure()

    @retry(RetryException, retries=5)
    def get_altitude(self):
        """
        Gets the current altitude as reported by the BMP085/BMP180 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from Bosch:

        https://ae-bst.resource.bosch.com/media/products/dokumente/bmp180/BST-BMP180-DS000-12~1.pdf

        :return: A float representing the current altitude.
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return self._bmp.read_altitude()

    @retry(RetryException, retries=2)
    def get_humidity(self):
        """
        Gets the current percentage of humidity as reported by the DHT11/DHT22 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from AOSONG:

        http://akizukidenshi.com/download/ds/aosong/AM2302.pdf

        :return: A float representing the percentage of humidity.
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, DHT22_PIN)[0]

    @retry(RetryException, retries=5)
    def get_pm(self):
        """
        Gets the current particular matter reading as a concentration per unit volume as reported by
        the Shinyei PPD42NJ sensor.

        For more information on how this reading is obtained, please see the
        official datasheet from Seeed Studio:

        http://www.seeedstudio.com/wiki/images/4/4c/Grove_-_Dust_sensor.pdf

        :return: A float representing the concentration of particles per unit volume.
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        # Flush the existing input buffer to ensure a fresh reading
        self._pm.flushInput()
        res = self._pm.read(24)
        
        # Add up each of the bytes in the frame
        sum = 0
        for i in range(0, 22):
            sum = sum + int(res[i].encode("hex"), 16)
        
        # Calculate the checksum using the last two bytes of the frame
        chksum = 256*int(res[22].encode("hex"), 16) + int(res[23].encode("hex"), 16)

        if sum != chksum:
            return None

        # Get the PM readings using the TSI standard
        pm1_upperb = int(res[4].encode("hex"), 16)
        pm1_lowerb = int(res[5].encode("hex"), 16)
        pm1 = 256*pm1_upperb + pm1_lowerb

        pm25_upperb = int(res[6].encode("hex"), 16)
        pm25_lowerb = int(res[7].encode("hex"), 16)
        pm25 = 256*pm25_upperb + pm25_lowerb

        pm10_upperb = int(res[8].encode("hex"), 16)
        pm10_lowerb = int(res[9].encode("hex"), 16) 
        pm10 = 256*pm10_upperb + pm10_lowerb 

        # Get the PM readings using the atmosphere as the standard
        pm1at_upperb = int(res[10].encode("hex"), 16)
        pm1at_lowerb = int(res[11].encode("hex"), 16)
        pm1at = 256*pm1at_upperb + pm1at_lowerb

        pm25at_upperb = int(res[12].encode("hex"), 16)
        pm25at_lowerb = int(res[13].encode("hex"), 16)
        pm25at = 256*pm25at_upperb + pm25at_lowerb

        pm10at_upperb = int(res[14].encode("hex"), 16)
        pm10at_lowerb = int(res[15].encode("hex"), 16)
        pm10at = 256*pm10at_upperb + pm10at_lowerb
        
        # Return the TSI standard readings
        return (pm1, pm25, pm10)

    @retry(RetryException, retries=5)
    def get_co2(self):
        """
        Gets the current CO2 reading as a concentration in parts per million (ppm) as reported by the MG-811
        sensor.

        For more information on how this reading is obtained, please see the
        official datasheet below:

        http://sandboxelectronics.com/files/SEN-000007/MG811.pdf

        :param retries: The number of times to retry to get a reading (default 5)
        :return: A float representing the concentration of CO2 (ppm).
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return None

    @retry(RetryException, retries=3)
    def get_co(self):
        """
        Gets the current voltage reading from the analog CO sensor. 
        
        :return: A voltage representing the current concentration of CO (ppm).
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return ADC.read(CO_PIN) * 1.8

    @retry(RetryException, retries=3)
    def get_no2(self):
        """
        Gets the current voltage reading from the analog NO2 sensor.

        :return: A voltage representing the current concentration of NO2. 
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return ADC.read(NO2_PIN) * 1.8

    @retry(RetryException, retries=5)
    def get_o3(self):
        """
        Gets the current O3 reading as a concentration in parts per million (ppm) as reported by the (fill
        this in here).

        For more information on how this reading is obtained, please see the
        official datasheet below:

        todo: Get datasheet for the specific O3 sensor we are using

        :return: A float representing the concentration of O3 (ppm).
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return None

    @retry(RetryException, retries=5)
    def get_uv(self):
        """
        Gets the current Ultra Violent Index (UVI) as reported by the Reyax UVI-01 sensor.

        For more information on how this reading is obtained, please see the
        official datasheet below:

        http://www.reyax.com/Module/UVI/UVI-01-E.pdf

        :return: A float representing the the current ultraviolet index rating.
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return None

    @retry(RetryException, retries=5)
    def get_lux(self):
        """
        Gets the current light intensity in lux as reported by the LDR sensor.

        For more information on how this reading is obtained, please see the
        official datasheet below:

        todo: Get datasheet for the specific LDR we are using

        :return: A float representing the current light intensity in lux
        :raises: exception.RetryException if no reading was obtained in the retry period.
        """

        return None

    def close(self):
        """
        Closes all of the open resources for this AirStation.

        This method should be invoked at the end of life for each AirStation
        object.
        """

        # Stop the GpsPoller in the extra thread if it is running
        if self._gpsp.running and self._mode == FIELD_MODE:
          self._gpsp.running = False
          self._gpsp.join()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager  method which is invoked on exit from the body of a
        with statement.

        See: https://www.python.org/dev/peps/pep-0343/
        """
        self.close()
