#!/usr/bin/python

#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      GeoffB
#
# Created:     13/04/2015
# Copyright:   (c) GeoffB 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import csv
#import uuid
import time
import random


def csv_writer(data, path):
    """csv_writer takes a list of intergers and a path to the file as input
    and output a csv file format of the data in the path location"""

    with open(path, "w") as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')
        for line in data:
            writer.writerow(line)

def floatify_data_string(temp_strings):

    """Take the raw data from the tank temps and convert them from string
    to integers"""

    temp_list = temp_string.split(", ")
    first_element = temps_list[0].replace("[", "")
    temps_list[0] = first_element
    float_temp_list = [round(float(tempstr, 1)) for tempstr in temps_list[0:-1]]
    return float_temp_list

def get_last_temps():

    """csv_reader takes a filename and returns the temp values in output.csv"""

    #"rt" is read text
    temps_list_final = []

    # change open('/home/pi/output.csv', 'rt')
    try:
	# so we try to open output.csv if success
        # then read the row in the file and floatify them
        # it would be nice to use our floatify method
        # instead of all that sloppy code
        with open("/home/worxi9/temp_manager/output.csv", "rt") as last_csv_temps:
            reader = csv.reader(last_csv_temps, delimiter='"',  skipinitialspace=True)
            _, temps, _= reader.next()
            temps_list = temps.split(", ")
            first_element = temps_list[0].replace("[","")
            temps_list[0] = first_element
            temps_list_final = [float(tempstr) for tempstr in temps_list[0:-1]]
        last_csv_temps.close()
    except: #if try to open output.csv fails then empty list
        temps_list_final = []
    return temps_list_final # so return to main call

def check_temp_range(tank_temps, min_temp, max_temp):

    """check_temp_range check data comming out of output.csv and make sure it
    in range"""
    #nope this does not create the new data if misssing

    num_tanks = len(tank_temps)
    for index in range(num_tanks):
        temp = tank_temps[index] 
        if temp <= min_temp:
            tank_temps[index] = min_temp
        if temp >= max_temp:
            tank_temps[index] = max_temp
    return tank_temps
            

def create_random_data_for_tanks(last_temp_list):

    """creat-random-data_for_tanks will creat new random data from old date+/-0.1
     to put into the tanks"""

    # ok create random data needs to make sure that if an
    # empty list is passed in that we seed a new list
    # so the temp list here should be empty lets print it out to
    #ok so our first step is to get the len of the list which
    # we know now is zero. So what happens in our for loop if
    # the range(0)?? lets start a python session in the othe rwindow and c
    data = []
     #8 tanks, 8 fake data temps
    for index in range(8):
        try:
            last_temp = last_temp_list[index] #create data +/-0.1 of last data
            new_temp = random.uniform(last_temp-0.1, last_temp+0.1)
        except: #seed a new start point of false temps
            #ok so if last_temp_list is null then this should exe
            new_temp = random.uniform(low, high)
        new_temp = round(new_temp, 1) #append seeds
        data.append(new_temp)
    return data
 

#----------------------------------------------------------------------

if __name__ == "__main__":


    # we need to generate a series of uid, timestamps and temp data
    low = 55.0   #range of valid temperature data
    high = 78.0
    last_temp_list = [] #save the last mock data to compare with newest
    list_accumulator = []
    datestamp = int(time.time())  # seconds since epoch unique id
    last_temp_list = get_last_temps() #return empty or full
    #if empty then check temp range will have to create new
    last_temp_list = check_temp_range(last_temp_list, low, high)
    data = create_random_data_for_tanks(last_temp_list)
    data.append(datestamp)    
    redis_insert_string = 'ZADD','Temps', datestamp, data  #create the redis commands for inseration
    path = "/home/worxi9/temp_manager/output.csv"
    list_accumulator.append(redis_insert_string) # accumulates list elments into single string for csv parsing
    csv_writer(list_accumulator, path)
