import argparse
from lib.airu.airstation import AirStation
from lib.airu.dbmodels import *


if __name__ == '__main__':
    """
    Main entry point for the AirU software layer for the Raspberry Pi.
    """

    # Create the command-line interface for this application
    parser = argparse.ArgumentParser(description='The airU main application.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enables verbose output to stdout.')
    parser.add_argument('-c', '--config', default='.', help='A directory containing the app configurations.')
    parser.add_argument('-l', '--log', help='The directory where logs should be written to.')

    args = parser.parse_args()

    db.init('air-metrics.db')
    db.connect()
    db.create_tables([AirMeasurement], True)

    with AirStation() as station:
        temp = station.get_temp()
        humidity = station.get_humidity()
        pressure = station.get_pressure()
        altitude = station.get_altitude()
        lat, lon = station.get_location()

    measurement = AirMeasurement(type='Temperature', value=temp, unit='C', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Humidity', value=humidity, unit='%', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Pressure', value=pressure, unit='Pascal', latitude=lat, longitude=lon)
    measurement.save()
    measurement = AirMeasurement(type='Altitude', value=altitude, unit='m', latitude=lat, longitude=lon)

    for m in AirMeasurement.select():
        print "Type: {0} Value: {1} Unit: {2} Lat: {3} Lon: {4} Date Added: {5} Uploaded: {6} Date Uploaded: {7}".format(
            m.type, m.value, m.unit, m.latitude, m.longitude, m.date_added, m.uploaded, m.date_uploaded)
