import argparse
import datetime
import time
import xlsxwriter
from lib.airu.airstation import AirStation

def generate_charts(workbook):
    """
    Generates the temperature, pressure, altitude, humidity, NOX, and CO charts in the supplied Excel workbook.

    :param workbook: The Excel workbook object where the charts should be placed
    """
    # Create a new chartsheet object for each chart.
    chartsheet1 = workbook.add_chartsheet("Temperature-Chart")
    chartsheet2 = workbook.add_chartsheet("Pressure-Chart")
    chartsheet3 = workbook.add_chartsheet("Altitude-Chart")
    chartsheet4 = workbook.add_chartsheet("Humidity-Chart")
    chartsheet5 = workbook.add_chartsheet("PM1-Chart")
    chartsheet6 = workbook.add_chartsheet("PM2.5-Chart")
    chartsheet7 = workbook.add_chartsheet("PM10-Chart")

    chart1 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'straight'})
    chart1.add_series({'name':       '=Sheet1!$B$1',
                       'values':     '=Sheet1!$B$2:$B${0}'.format(row),
                       'categories': '=Sheet1!$A$2:$A${0}'.format(row),
                       'marker': {'type': 'diamond',
                                  'size': 8}})
    chart1.set_title({'name': 'Time vs. Temperature'})
    chart1.set_x_axis({'name': 'Time (UTC)',
                       'date_axis': True,
                       'num_format': 'hh:mm:ss'})
    chart1.set_y_axis({'name': 'Temperature (C)'})
    chart1.set_legend({'none': True})

    # Set an Excel chart style.
    chart1.set_style(11)
    chartsheet1.set_chart(chart1)

    chart2 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'straight'})
    chart2.add_series({'name':       '=Sheet1!$C$1',
                       'values':     '=Sheet1!$C$2:$C${0}'.format(row),
                       'categories': '=Sheet1!$A$2:$A${0}'.format(row),
                       'marker': {'type': 'diamond',
                                  'size': 8}})
    chart2.set_title({'name': 'Time vs. Pressure'})
    chart2.set_x_axis({'name': 'Time (UTC)',
                       'date_axis': True,
                       'num_format': 'hh:mm:ss'})
    chart2.set_y_axis({'name': 'Pressure (Pa)'})
    chart2.set_legend({'none': True})

    # Set an Excel chart style.
    chart2.set_style(11)
    chartsheet2.set_chart(chart2)

    chart3 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'straight'})
    chart3.add_series({'name':       '=Sheet1!$D$1',
                       'values':     '=Sheet1!$D$2:$D${0}'.format(row),
                       'categories': '=Sheet1!$A$2:$A${0}'.format(row),
                       'marker': {'type': 'diamond',
                                  'size': 8}})
    chart3.set_title({'name': 'Time vs. Altitude'})
    chart3.set_x_axis({'name': 'Time (UTC)',
                       'date_axis': True,
                       'num_format': 'hh:mm:ss'})
    chart3.set_y_axis({'name': 'Altitude (m)'})
    chart3.set_legend({'none': True})

    # Set an Excel chart style.
    chart3.set_style(11)
    chartsheet3.set_chart(chart3)

    chart4 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'straight'})
    chart4.add_series({'name':       '=Sheet1!$E$1',
                       'values':     '=Sheet1!$E$2:$E${0}'.format(row),
                       'categories': '=Sheet1!$A$2:$A${0}'.format(row),
                       'marker': {'type': 'diamond',
                                  'size': 8}})
    chart4.set_title({'name': 'Time vs. Humidity'})
    chart4.set_x_axis({'name': 'Time (UTC)',
                       'date_axis': True,
                       'num_format': 'hh:mm:ss'})
    chart4.set_y_axis({'name': 'Humidity (%)'})
    chart4.set_legend({'none': True})

    # Set an Excel chart style.
    chart4.set_style(11)
    chartsheet4.set_chart(chart4)

    chart5 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'straight'})
    chart5.add_series({'name':       '=Sheet1!$F$1',
                       'values':     '=Sheet1!$F$2:$F${0}'.format(row),
                       'categories': '=Sheet1!$A$2:$A${0}'.format(row),
                       'marker': {'type': 'diamond',
                                  'size': 8}})
    chart5.set_title({'name': 'Time vs. PM1'})
    chart5.set_x_axis({'name': 'Time (UTC)',
                       'date_axis': True,
                       'num_format': 'hh:mm:ss'})
    chart5.set_y_axis({'name': 'ug/m3'})

    # Set an Excel chart style.
    chart5.set_style(11)
    chartsheet5.set_chart(chart5)

    chart6 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'straight'})
    chart6.add_series({'name':       '=Sheet1!$G$1',
                       'values':     '=Sheet1!$G$2:$G${0}'.format(row),
                       'categories': '=Sheet1!$A$2:$A${0}'.format(row),
                       'marker': {'type': 'diamond',
                                  'size': 8}})
    chart6.set_title({'name': 'Time vs. PM2.5'})
    chart6.set_x_axis({'name': 'Time (UTC)',
                       'date_axis': True,
                       'num_format': 'hh:mm:ss'})
    chart6.set_y_axis({'name': 'ug/m3'})

    # Set an Excel chart style.
    chart6.set_style(11)
    chartsheet6.set_chart(chart6)

    chart7 = workbook.add_chart({'type': 'scatter',
                                 'subtype': 'straight'})
    chart7.add_series({'name':       '=Sheet1!$H$1',
                       'values':     '=Sheet1!$H$2:$H${0}'.format(row),
                       'categories': '=Sheet1!$A$2:$A${0}'.format(row),
                       'marker': {'type': 'diamond',
                                  'size': 8}})
    chart7.set_title({'name': 'Time vs. PM10'})
    chart7.set_x_axis({'name': 'Time (UTC)',
                       'date_axis': True,
                       'num_format': 'hh:mm:ss'})
    chart7.set_y_axis({'name': 'ug/m3'})

    # Set an Excel chart style.
    chart7.set_style(11)
    chartsheet7.set_chart(chart7)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outfile", default=time.strftime("%Y%m%d-%H%M%S")+".xlsx", help="The Excel output filename.")
    parser.add_argument("-f", "--frequency", type=int, default=60, help="The frequency at which measurements should be captured.")

    args = parser.parse_args()

    out_filename = args.outfile
    frequency = args.frequency

    try:
        print "Press CTRL+C at any time to terminate this process..\n"

        station = AirStation()

        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook(out_filename)
        worksheet = workbook.add_worksheet()

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})

        # Create a date format object
        date_format = workbook.add_format({'num_format': 'hh:mm:ss'})

        # Write the header with formatting.
        worksheet.write_row(0, 0, ("Time", "Temperature", "Pressure", "Altitude", "Humidity", "PM1", "PM2.5", "PM10"), bold)

        # Start collecting the continuous stream of data
        row = 1
        while True:

            # Split the line into the appropriate sensor readings
            time_stamp = datetime.datetime.now()
            temperature        = station.get_temp()
            humidity           = station.get_humidity()
            pressure           = station.get_pressure()
            altitude           = station.get_altitude()
            (pm1, pm2_5, pm10) = station.get_pm()

            # Print out the sensor readings
            print "Temperature: {0} (*C)".format(temperature)
            print "Pressure:    {0} (Pa)".format(pressure)
            print "Altitude:    {0} (m)".format(altitude)
            print "Humidity:    {0} (%)".format(humidity)
            print "PM1.0:       {0} (ug/m3)".format(pm1)
            print "PM2.5:       {0} (ug/m3)".format(pm2_5)
            print "PM10:        {0} (ug/m3)\n".format(pm10)

            # Write the data to the Excel worksheet and increment the row
            worksheet.write_datetime(row, 0, time_stamp, date_format)
            worksheet.write_number(row, 1, temperature)
            worksheet.write_number(row, 2, pressure)
            worksheet.write_number(row, 3, altitude)
            worksheet.write_number(row, 4, humidity)
            worksheet.write_number(row, 5, pm1)
            worksheet.write_number(row, 6, pm2_5)
            worksheet.write_number(row, 7, pm10)
            row += 1

            time.sleep(frequency)

    except KeyboardInterrupt:
        print "\nCTRL+C Signal Caught!"
        print "Terminating this Process."
    finally:

        generate_charts(workbook)

        # Close the Excel workbook
        workbook.close()
