#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Thao Nguyen
#
# Created:     06/05/2015
# Copyright:   (c) Thao Nguyen 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time
import redis
import itertools
import datetime
import csv
import redis_to_html

# outline of csv outputer
# 1. Date selectable range user input
# 2. Pull data from redis based on those ranges
# 3. Output the redis data in csv format

#instead of define, use class save data during transform, change range of data;
# instead of save as output.csv file, will save as csv in redis memory.

class Temperature(object):

    """Temperatures takes a date range of values based on user input and
    pools the redis database for the temp valuse and outputs the data to csv"""

    def __init__(self):
        pass

    def validate_user_input(self, date_string):

        """Check to see if the date that was entered is parsable
        by datetime if not return false"""

	# take the user string and see if it can be parsed
        # as a date, if it can return True if it cant the user input
        # is not valid and must be fixed before continuing
        try:
            datetime.datetime.strptime(date_string, "%m/%d/%Y")
            return True
        except ValueError:
            return False

    def valid_redis_range(self, redis_object, start_date, end_date):

        """get start and end date of redis temp data and compare the
        user input to that range. If user input not in that range
        return message to user that input out of range"""

        redis_range = iter(redis_object.zrange("Temps", 0, -1, withscores=True))
        # so we need the length of the redis database so we can send
        # that to the islice method which gives us the final element of
        # the iterator
        num_temps = int(redis_object.zcard("Temps"))
        #print num_temps, 'this is num temps' #this worked 
        redis_start = itertools.islice(redis_range, 0, 1) 
        # note: islice() requires a span of 2 to get the end value
        redis_end = itertools.islice(redis_range, num_temps-2, num_temps)
        start_with_score =  list(redis_start)[0] #here is print the itertools.slice object
        end_with_score = list(redis_end)[0]
        _, start_score = start_with_score
        _, end_score = end_with_score
        return start_score, end_score

    def validate_user_range(self, epoch_range, user_range):

	"""Take in a user inputted start and end date and compare it to
        the start and end date of the redis database"""

	db_start, db_end = epoch_range
        start_input, end_input = user_range

	if (db_start <= start_input <= db_end and
           db_start <= end_input <= db_end):
               return True
        else:
            return False
	

    def user_input(self):

        """Get the input from the user"""
        # date range in format "10/10/2015 10/22/2015"

        self.date_range = raw_input("Enter date range: ") # self is like an unique id
        return self.date_range

    def convert_string_to_epoch(self, date_range):

        """Takes a user entered date range and converts each to an epoch score for
        retreiving the range of date from the redis database"""

	# date_range looks like "05/14/2015 05/15/2015" type string
        self.date_pattern = "%m/%d/%Y %H:%M:%S" #create pattern to parse date
        self.split_date = date_range.split(" ") # split the date range into two
        self.start = self.split_date[0] + " 00:00:00" #add empty time to the date
        self.end = self.split_date[1] + " 00:00:00" # to match our pattern
        self.start_score = time.strptime(self.start, self.date_pattern) #convert
        self.end_score = time.strptime(self.end, self.date_pattern) # to time/date object
        self.epoch_start = float(time.mktime(self.start_score)) #convert to epoch float
        self.epoch_end = float(time.mktime(self.end_score))

        return self.epoch_start, self.epoch_end

    def convert_tempstring_to_float(self, temp_string):

	""" convert_tempstring_to_float takes a string from the redis db and
        converts it from string type to individual float temperatures"""

        temp_list = temp_string.split(", ")
        # the string from redis still has the list brackets so
        # strip them out and replace with nothing ""
        first_element = temp_list[0].replace("[", "")
        temp_list[0] = first_element

        # We don't need to get the last element so 
        # the following code is not needed
        # last_element = temp_list[-1].replace("]", "")
        # temp_list[-1] = last_element

	# convert each list item to a float except final element
        temp_floats = [float(temp) for temp in temp_list[:-1]]
        return temp_floats


    def convert_all_redis_to_float(self, raw_redis_data):

        """This iterates through each of the rows from the redis db and
        calls the convert_tempstring_to_float on each row"""

        save_data = []
        for data in raw_redis_data:
            floated_data = self.convert_tempstring_to_float(data)
            save_data.append(floated_data)
        return save_data


    def get_redis_range(self, redis_object, epochs):
     
        """Pulls data out of the redis database. Takes the connection to the redis db
        and the range of epoch scores to pull out. zrangebyscores()"""

        self.start_score = epochs[0]
        self.end_score = epochs[1]

        redis_data = redis_object.zrangebyscore("Temps", self.start_score, self.end_score)
        if redis_data:
            return redis_data
        else:
            return 0

    def csv_writer(self, data):

        """csv_writer takes a list of integers and a path to the file as input
        and output a csv file format of the data in the path location"""

        path = "range.csv"
        with open(path, "w") as csv_file:
            writer = csv.writer(csv_file, delimiter=' ')
            for line in data:
                writer.writerow(line)



if __name__ == '__main__':

    redis_connection = redis.StrictRedis(host = "localhost", port=6379, db=0)
    temp_instance = Temperature()
    # get user input
    start_date = temp_instance.user_input()
    end_date = temp_instance.user_input()
    # take the user input and call validate_user_input
    # to make sure its an actual parsable date

    if (temp_instance.validate_user_input(start_date) and
        temp_instance.validate_user_input(end_date)):
        #our call to convert_string_to_epoch expects a string of start date
        # and end date with exactly one space in between. 
        # echo we can deprecitate the below later its redundante to 
        # add these strings together only to take them back apart
        # in the call to convert_string_to_epoch
        user_input = start_date + " " + end_date #add user strings together
        user_range = temp_instance.convert_string_to_epoch(user_input)
        db_range = temp_instance.valid_redis_range(redis_connection, start_date, end_date)
	# validate that the input range is found in redis range
        valid_dates = temp_instance.validate_user_range(db_range, user_range)

        if valid_dates: #if yes, True
            raw_redis = temp_instance.get_redis_range(redis_connection, user_range)

        if raw_redis:
    	    redis_float_data = temp_instance.convert_all_redis_to_float(raw_redis)
	    temps_by_tank  = redis_to_html.get_temps_by_tank(redis_float_data, 8)
            for tank in temps_by_tank:
                print tank
                print " "    
        # temp_instance.csv_writer(csv_ready_data)
        else:
            print 'no data'
