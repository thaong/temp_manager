#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thao Nguyen
#
# Created:     12/03/2015
# Copyright:   (c) Thao Nguyen 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Try to upload a file to Rpi and run it
import datetime
import csv
import time


f= open('temps.csv', 'w')
csv.register_dialect('custom', delimiter=' ', skipinitialspace=True)
writer = csv.writer(f, dialect='custom')

for i in range(10):
    temp_list = []

    date_value = datetime.datetime.now() #this funstion get the time
    date_string = "%s/%s/%s" % (date_value.month,
                                date_value.day,
                                date_value.year)
    temp_list.append(date_string)


        # Get the timestamp, parse time into strings and append to temp list
    time_string = "%s:%s:%s" % (date_value.hour,
                                date_value.minute,
                                date_value.second)
    temp_list.append(time_string)
    temperature =  int(open('/sys/class/thermal/thermal_zone0/temp').read())/1000.0
    temp_list.append(temperature)

    print temp_list
    writer.writerow(temp_list)


    time.sleep(.1)