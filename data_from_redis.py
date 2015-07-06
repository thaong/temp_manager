import redis
import time
import datetime
import numpy as np
from bokeh.plotting import figure, output_file, show, HBox, VBox
from bokeh.document import Document

# Geoffs recipe for data_from_redis.py
# Make sure that all of your functions are defined at the top before you make
# any calls to those functions. Then make sure that when you
# call the functions that they are called in the order outlined below

# 1. Create a redis database object - redis_object
# 2. Cakeup a range of dates to pull from redis db
# 3. Convert those dates into epoch score with  convert_date_to_epochscore
# 4. Use the converted dates to pull out the range from redis redis_object.zrange()
# 5. Convert the redis data strings into integers with convert_tempstring_to_integers
# 6. Format the redis data by tank number with  get_temps_by_tank()
# 7. Assign the time and temperature values from the tank numbers
# The rest is TBA

#create a redis database connection object to send db queries

# the below range is just an example of getting a certain range
# from a redis_object. It is not used in the current program
#range_data = redis_object.zrange("Temps", 0, 10)
#for Temps in range_data:
#    print Temps

def convert_date_to_epochscore(date_string):

    """conver_date_to_epochscore takes a human readable data and
     converts it to seconds since epoch.  We use that second since
     epoch as a score in the redis database"""

    date_pattern = '%Y/%m/%d %H:%M:%S'
    time_stamp = time.strptime(date_string, date_pattern)
    epoch_seconds = float(time.mktime(time_stamp))
   # epoch_seconds = float(time.mktime(time.strptime(data_string, date_pattern)))
    return epoch_seconds

def convert_epoch_to_date(epoch_int):

    """convert_epoch_to_date takes an seconds to epoch integer and converts
    it to a human readable format"""

    human_readable_date = float(
        datetime.datetime.fromtimestamp(epoch_int).strftime(
        '%Y/%m/%d %H:%M:%S'))
#    print human_readable_date, "this is human_readable_date"
    return human_readable_date

def convert_tempstring_to_floats(temp_string):

    temp_list = temp_string.split(", ")

    first_element = temp_list[0].replace("[", "")
    temp_list[0] = first_element

    last_element = temp_list[-1].replace("]", "")
    temp_list[-1] = last_element

    temp_floats = [float(temp) for temp in temp_list]
    return temp_floats

def convert_redis_data_to_floats(range_data2):
    
    """convert_redis_data_to_integers using temp_floats to convert the 
    entire data from redis into row and reconized by timestamp"""
    
    raw_temp_list = []
   
    for data in range_data2:
        temp_floats = convert_tempstring_to_floats(data)
        raw_temp_list.append(temp_floats)
    return raw_temp_list 

def get_temps_by_tank(tank_temp_list):

    """get_temps_by_tank takes a list of redis database range temperatures and
    pulls out column data."""

    # now initialize the return variable
    temps_by_tank = []
    
    for index in range(9):  #8 temps and 1 epoch second values = 9 range items
        temp_temps = [tmp[index] for tmp in tank_temp_list]  #pull column data
        temps_by_tank.append(temp_temps)
    return temps_by_tank

if __name__ == '__main__':

    #create a human readable date that we can convert to epoch
   # start_range = '2015/04/30 12:50:10'
   # end_range = '2015/04/30 13:10:10'

    # convert the human readable date for use in the zrange redis call
   # start_epoch = convert_date_to_epochscore(start_range)
   # end_epoch = convert_date_to_epochscore(end_range)
    redis_object = redis.StrictRedis(host='localhost', port=6379, db=0)
    #  query the redis database with a range of dates
    most_recent_data = redis_object.zrange('Temps', -60, -1)
    #ok so we have range data now step 2 is to convert that from raw to int
    tank_temps = convert_redis_data_to_floats(most_recent_data)
    temps_by_tank = get_temps_by_tank(tank_temps)
   # for element in temps_by_tank:
#        print element

    x_axis_time_stamps = temps_by_tank[-1]

    x_axis_time_stamps = [datetime.datetime.fromtimestamp(ts) for ts in x_axis_time_stamps]
#create date time object to a bokeh time line 
    x_axis_time_stamps = [np.datetime64(dt).astype(long)/1000 for dt in x_axis_time_stamps]
   # print x_axis_time_stamps
 
    y0_temps = temps_by_tank[0]
    y1_temps = temps_by_tank[1]
    y2_temps = temps_by_tank[2]
    y3_temps = temps_by_tank[3]
    y4_temps = temps_by_tank[4] 
    y5_temps = temps_by_tank[5]
    y6_temps = temps_by_tank[6]
    y7_temps = temps_by_tank[7]
    y8_temps = temps_by_tank[8]

    Document = Document()
    output_file("/var/www/index.html")
    attrib_dict = dict(width=300, height=300, x_axis_type="datetime")
    line_dict = dict(size=12, alpha=0.5)

    plot0 = figure(title="Tank 1", **attrib_dict)
    plot1 = figure(title="Tank 2", **attrib_dict)
    plot2 = figure(title="Tank 3", **attrib_dict)
    plot3 = figure(title="Tank 4", **attrib_dict)
    plot4 = figure(title="Tank 5", **attrib_dict)
    plot5 = figure(title="Tank 6", **attrib_dict)
    plot6 = figure(title="Tank 7", **attrib_dict)
    plot7 = figure(title="Tank 8", **attrib_dict)

    plot0.line(x_axis_time_stamps, y0_temps, color="black", **line_dict)
    plot1.line(x_axis_time_stamps, y1_temps, color="red", **line_dict)
    plot2.line(x_axis_time_stamps, y2_temps, color="green", **line_dict)
    plot3.line(x_axis_time_stamps, y3_temps, color="blue", **line_dict)
    plot4.line(x_axis_time_stamps, y4_temps, color="violet", **line_dict)
    plot5.line(x_axis_time_stamps, y5_temps, color="blue", **line_dict)
    plot6.line(x_axis_time_stamps, y6_temps, color="red", **line_dict)
    plot7.line(x_axis_time_stamps, y7_temps, color="purple", **line_dict)


    show(VBox(HBox(plot0,plot1,plot2,plot3), HBox(plot4,plot5,plot6,plot7)))

