import redis
import time
import datetime
import numpy as np
from bokeh.plotting import figure, output_file, show, HBox, VBox
from bokeh.document import Document

""" 1. Create a redis database object - redis_object
    2. Pull 60 most recent temp values from redis db redis_object.zrange()
    3. Convert the redis data strings into integers with convert_tempstring_to_integers
    6. Pull out the temp data by tank number with  get_temps_by_tank()
    7. Assign the x an y axis values to bokeh lists
    8. Create  bokeh plots and index.html file then copy to /var/www for nginx access
"""

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
    return human_readable_date

def convert_tempstring_to_floats(temp_string):

    """Clean up the data string from redis and convert the list elements
    to floats"""

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

def get_temps_by_tank(tank_temp_list, num_vals=9):

    """get_temps_by_tank takes a list of redis database range temperatures and
    pulls out column data."""

    # now initialize the return variable
    temps_by_tank = []
    
    for index in range(num_vals):  #8 temps and 1 epoch second values = 9 range items
        temp_temps = [tmp[index] for tmp in tank_temp_list]  #pull column data
        temps_by_tank.append(temp_temps)
    return temps_by_tank

if __name__ == '__main__':

    # create redis connection
    redis_object = redis.StrictRedis(host='localhost', port=6379, db=0)
    #  query the redis database with a range of dates
    most_recent_data = redis_object.zrange('Temps', -40, -1)
    # convert each row from redis call into floats
    tank_temps = convert_redis_data_to_floats(most_recent_data)
    # pull out the tank temps and group into y axis lists
    temps_by_tank = get_temps_by_tank(tank_temps)
    # pull out the last elment from the temps by tank which is epoch score
    x_axis_time_stamps = temps_by_tank[-1]
    # adjust the timestamps to central time -18000 seconds or 5 hours
    x_axis_time_stamps = [epoch - 18000 for epoch in x_axis_time_stamps]
    #create the x axis for bokeh
    x_axis_time_stamps = [datetime.datetime.fromtimestamp(ts) for ts in x_axis_time_stamps]
    #create date time object to a bokeh time line 
    x_axis_time_stamps = [np.datetime64(dt).astype(long)/1000 for dt in x_axis_time_stamps]

    # assign each tank its list of temperatures 
    y0_temps = temps_by_tank[0]
    y1_temps = temps_by_tank[1]
    y2_temps = temps_by_tank[2]
    y3_temps = temps_by_tank[3]
    y4_temps = temps_by_tank[4] 
    y5_temps = temps_by_tank[5]
    y6_temps = temps_by_tank[6]
    y7_temps = temps_by_tank[7]
    y8_temps = temps_by_tank[8]

    #create the bokeh document to populate with plots and index.html file
    Document = Document()
    output_file("/var/www/index.html")
    # create some attributes to save typing when formating plots
    attrib_dict = dict(width=300, height=300, x_axis_type="datetime")
    line_dict = dict(size=12, alpha=0.5)

    # create the figures that hold each tanks plot
    plot0 = figure(title="Tank 1", **attrib_dict)
    plot1 = figure(title="Tank 2", **attrib_dict)
    plot2 = figure(title="Tank 3", **attrib_dict)
    plot3 = figure(title="Tank 4", **attrib_dict)
    plot4 = figure(title="Tank 5", **attrib_dict)
    plot5 = figure(title="Tank 6", **attrib_dict)
    plot6 = figure(title="Tank 7", **attrib_dict)
    plot7 = figure(title="Tank 8", **attrib_dict)

    # create the lines that go on the figure with attributes
    plot0.line(x_axis_time_stamps, y0_temps, color="black", **line_dict)
    plot1.line(x_axis_time_stamps, y1_temps, color="red", **line_dict)
    plot2.line(x_axis_time_stamps, y2_temps, color="green", **line_dict)
    plot3.line(x_axis_time_stamps, y3_temps, color="blue", **line_dict)
    plot4.line(x_axis_time_stamps, y4_temps, color="violet", **line_dict)
    plot5.line(x_axis_time_stamps, y5_temps, color="blue", **line_dict)
    plot6.line(x_axis_time_stamps, y6_temps, color="red", **line_dict)
    plot7.line(x_axis_time_stamps, y7_temps, color="purple", **line_dict)

    # tell bokeh to create the plots and display them
    show(VBox(HBox(plot0,plot1,plot2,plot3), HBox(plot4,plot5,plot6,plot7)))

