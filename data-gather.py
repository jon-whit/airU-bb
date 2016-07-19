"""
data-gather.py

Author: Jonathan Whitaker
Email: jon.b.whitaker@gmail.com
Date: April 21, 2016

data-gather.py is an integral part of the AirU toolchain, serving as the script
which collects the data from the various sensors onboard an AirU station. This 
script is designed to run using a Cron. It was designed to write the data to an
internal database if the station is set to run in Field Mode, or it will write 
the data to a CSV file named by the current time and date if the station is in 
Lab Mode.
"""
import logging
import datetime
import sys
import time
import serial
import Adafruit_BMP.BMP085 as BMP085
import Adafruit_BBIO.GPIO as GPIO
from lib.airu import utils
from lib.airu import airstation
from lib.airu.airstation import AirStation
from lib.airu.dbmodels import *

# Setup the Logging interface for this script
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

if __name__ == '__main__':
    
    # Setup logging
    logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    logfilename = "/var/log/{0}.log".format(time.strftime("%m-%d-%Y"))
    fileHandler = logging.FileHandler(logfilename)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    
    # Setup the GPIO input pin for the mode switch
    GPIO.setup(airstation.MODE_SWITCH, GPIO.IN)
    
    # If the mode switch is "high", the station is in field mode
    if GPIO.input(airstation.MODE_SWITCH):
        mode = airstation.FIELD_MODE
    else:
        mode = airstation.LAB_MODE

    # Sample the sensors
    rootLogger.info('Capturing Measurements from the Onboard Sensors...')
    pm_ser = serial.Serial(port=airstation.PM_PORT, baudrate=9600, rtscts=True, dsrdtr=True)
    with AirStation(BMP085.BMP085(), utils.GpsPoller(), pm_ser, mode) as station:
        temp = station.get_temp()
        rootLogger.info('Temperature:      {0:0.1f} C'.format(temp))
        humidity = station.get_humidity()
        rootLogger.info('Humidity:         {0:0.1f} %'.format(humidity))
        pressure = station.get_pressure()
        rootLogger.info('Pressure:         {0:0.1f} Pa'.format(pressure))
        altitude = station.get_altitude()
        rootLogger.info('Altitude:         {0:0.1f} m'.format(altitude))
        
        if mode == airstation.FIELD_MODE:
            lon, lat = station.get_location()
            rootLogger.info('Latitude:         {0:0.1f} deg'.format(lat))
            rootLogger.info('Longitude:        {0:0.1f} deg'.format(lon))

        (pm1, pm25, pm10) = station.get_pm()
        rootLogger.info('PM1.0:            {0:0.1f} ug/m3'.format(pm1))
        rootLogger.info('PM2.5:            {0:0.1f} ug/m3'.format(pm25))
        rootLogger.info('PM10:             {0:0.1f} ug/m3'.format(pm10))
    rootLogger.info('Done Capturing Measurements.')
    
    """
    Check the operation mode. If the station is in field mode, write the measurements 
    to the internal database. Otherwise, write the measurements to a CSV file named by 
    the current date and time.
    """ 
    if mode == airstation.FIELD_MODE:
        rootLogger.info('Station Set to Field Mode.')
        rootLogger.info('Setting Up Internal Database...')
        db.init('/root/air-metrics.db')
        db.connect()
        db.create_tables([AirMeasurement], True)
        rootLogger.info('Database Setup Complete.')
        
        # Save the captured measurements to the database
        rootLogger.info('Saving Captured Measurements to the Database...')
        measurement = AirMeasurement(type='Temperature', value=temp, unit='C', latitude=lat, longitude=lon)
        measurement.save()
        measurement = AirMeasurement(type='Humidity', value=humidity, unit='%', latitude=lat, longitude=lon)
        measurement.save()
        measurement = AirMeasurement(type='Pressure', value=pressure, unit='Pascal', latitude=lat, longitude=lon)
        measurement.save()
        measurement = AirMeasurement(type='Altitude', value=altitude, unit='M', latitude=lat, longitude=lon)
        measurement.save()
        measurement = AirMeasurement(type='PM1.0', value=pm1, unit='UG/M3', latitude=lat, longitude=lon)
        measurement.save()
        measurement = AirMeasurement(type='PM2.5', value=pm25, unit='UG/M3', latitude=lat, longitude=lon)
        measurement.save()
        measurement = AirMeasurement(type='PM10.0', value=pm10, unit='UG/M3', latitude=lat, longitude=lon)
        measurement.save()
        rootLogger.info('Measurements Saved.\n')
    else:
        rootLogger.info('Station Set to Lab Mode.')
        # Otherwise append the measurement to a file with the current date and time
        outputfile = "/media/sdcard/{0}.csv".format(time.strftime("%m-%d-%Y"))
        rootLogger.info("Opening CSV File '{0}' for Writing...".format(outputfile))
        fh = open(outputfile, 'a')
        
        rootLogger.info("Writing Sample to File...")
        datastr = "{0},{1},{2},{3},{4},{5},{6}\n".format(temp, humidity, pressure, altitude, pm1, pm25, pm10)
        fh.write(datastr)
        rootLogger.info("Sample Successfully Written.\n")
        
