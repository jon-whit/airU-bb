import datetime
from peewee import *

db = SqliteDatabase(None)

class BaseModel(Model):
    class Meta:
        database = db

class AirMeasurement(BaseModel):
    """
    An AirMeasurement model represents a single data point collected by an airU air quality
    station.

    An AirMeasurement entry has the following fields:
        * type - The type of measurement being collected (e.g. CO, CO2, PM, Humidity, Temperature, etc..)
        * value - The value of the measurement
        * unit - The metric unit associated with the measurement (e.g. ppm, %, C, Pascals, etc..)
        * latitude - The latitudinal coordinate where this measurement was taken from
        * longitude - The longitudinal coordinate where this measurement was taken from
        * date_added - The timestamp when this measurement was collected
        * uploaded - A boolean field indicating if the measurement was uploaded


    """

    type = CharField(choices=['CO', 'CO2', 'O3', 'PM', 'NO2' 'Humidity', 'Temperature', 'Pressure', 'Altitude'])
    value = FloatField()
    unit = CharField()
    latitude = DoubleField()
    longitude = DoubleField()
    date_added = DateTimeField(default=datetime.datetime.now)
    uploaded = BooleanField(default=False)
    date_uploaded = DateTimeField(null=True)