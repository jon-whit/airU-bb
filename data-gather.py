import argparse
import logging
import datetime
import sys
from lib.airu.airstation import AirStation
from lib.airu.dbmodels import *

# Setup the Logging interface for this app
rootLogger = logging.getLogger()
rootLogger.setLevel(logging.INFO)

if __name__ == '__main__':
    """
    """

    # Create the command-line interface for this application
    parser = argparse.ArgumentParser(description='The airU main application.')
    parser.add_argument('-c', '--config', default='.', help='A directory containing the app configurations.')
    parser.add_argument('-l', '--log', help='The path where logs should be written to. (defaults to the current directory)')

    args = parser.parse_args()

    # Setup logging
    logFormatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    if args.log:
        filename = "{0}/{1}.log".format(args.log, datetime.datetime.now().strftime("%m-%d-%Y"))
    else:
        filename = "{0}.log".format(datetime.datetime.now().strftime("%m-%d-%Y"))
    fileHandler = logging.FileHandler(filename)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    # Create the internal database for this station
    rootLogger.info('Setting Up Internal Database...')
    db.init('/root/air-metrics.db')
    db.connect()
    db.create_tables([AirMeasurement], True)
    rootLogger.info('Database Setup Complete.')

    rootLogger.info('Capturing Measurements from the Onboard Sensors...')
    with AirStation() as station:
        temp = station.get_temp()
        rootLogger.info('Temperature:      {0:0.1f} C'.format(temp))
        humidity = station.get_humidity()
        rootLogger.info('Humidity:         {0:0.1f} %'.format(humidity))
        pressure = station.get_pressure()
        rootLogger.info('Pressure:         {0:0.1f} Pa'.format(pressure))
        altitude = station.get_altitude()
        rootLogger.info('Altitude:         {0:0.1f} m'.format(altitude))
        #lon, lat = station.get_location()
        lon, lat = (41.2, 141.1)
        rootLogger.info('Latitude:         {0:0.1f} deg'.format(lat))
        rootLogger.info('Longitude:        {0:0.1f} deg'.format(lon))
        (pm1, pm25, pm10) = station.get_pm()
        rootLogger.info('PM1.0:            {0:0.1f} ug/m3'.format(pm1))
        rootLogger.info('PM2.5:            {0:0.1f} ug/m3'.format(pm25))
        rootLogger.info('PM10.0:            {0:0.1f} ug/m3'.format(pm10))
    rootLogger.info('Done Capturing Measurements.')

    # Save the captured measurements to the database
    rootLogger.info('Saving Captured Measurements to the Database...')
    measurement = AirMeasurement(type='Temperature', value=temp, unit='C', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Humidity', value=humidity, unit='%', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Pressure', value=pressure, unit='Pascal', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Altitude', value=altitude, unit='m', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='PM1.0', value=pm1, unit='ug/m3', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='PM2.5', value=pm25, unit='ug/m3', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='PM10.0', value=pm10, unit='ug/m3', latitude=lat, longitude=lon)
    measurement.save()
    rootLogger.info('Measurements Saved.\n')

