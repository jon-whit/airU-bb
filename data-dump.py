import argparse
import xlsxwriter
from lib.airu.dbmodels import *
from playhouse.csv_loader import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--outputfile', help='The output filename (defaults to current timestamp).')
    parser.add_argument('-c', '--csv', action='store_true', help='Write the output as a CSV file.')

    args = parser.parse_args()

    filename = '{0}'.format(datetime.datetime.now())
    if args.outputfile:
        filename = args.outputfile

    db.init('/root/air-metrics.db')
    db.connect()
    db.create_tables([AirMeasurement], True)

    if args.csv:
        # Generate a CSV file containing all of the data collected up to this point 
        with open(filename + '.csv', 'w') as fh:
            query = AirMeasurement.select().order_by(AirMeasurement.date_added)
            dump_csv(query, fh)
    else:
        # Generate an Excel file containing all of the data collected up to this point
        
        # Create an new Excel file and add a worksheet for each data type.
        workbook = xlsxwriter.Workbook(filename + '.xlsx')
        
        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Create a date format object
        date_format = workbook.add_format({'num_format': 'hh:mm:ss'})

        # Add a worksheet for each data type and insert the data into the worksheet
        types = ['PM1.0', 'PM2.5', 'PM10.0', 'Humidity', 'Temperature', 'Pressure', 'Altitude']
        for type in types:
            worksheet = workbook.add_worksheet(type)

            worksheet.write_row(0, 0, ("Time", type), bold) 

            row = 1
            for entry in AirMeasurement.select().where(AirMeasurement.type == type).order_by(AirMeasurement.date_added):
                worksheet.write_datetime(row, 0, entry.date_added, date_format)
                worksheet.write_number(row, 1, entry.value)
                row += 1

        workbook.close()
