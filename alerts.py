#/usr/bin/python

""" Create the alerts for the temperature ranges. If we trigger an
    alert we send an email and turn the plot red.
    1.  <-25C...35C-> temp out of range 77F to 95F
    2. 1.2C in 1 hour
"""

import smtplib
from collections import namedtuple

# get the last hours data
# get all current temps
# check last hour for gradient movement
# check last hour for over/under range
# if either state
# send email
# change plot color to red


# we need to take the last 12 of each tank and check for
# temp range and gradient

def get_last_hour_data(temps_by_tank):

    """get_last_hour_data takes a list of tank temps from temps_by_tank
     in redis to check for alert"""

    return temps_by_tank[-12,-1]

def check_tank_for_gradient_alert(temps_by_tank):

    """will compare the first and the last temps for temperature change"""

    # this takes temperatures that are already separated out by tank
    # will not work with test_data.py
    first_temps = temps_by_tank[0]
    last_temps = temps_by_tank[-1]
    temp_dif = abs(first_temps - last_temps)
    if temp_dif >= 0.6:
        return True
    else:
        return False

def check_tank_for_temp_outofrange(temps_by_tank):

    """will check if temp between 25 to 35 celcius"""

    # this just checks last tank temp so will not work with test_data.py
    last_temp = temps_by_tank[-1]
    if 25<= last_temp<=35:
       return True
    else:
       return False

def compare_temps_to_threshold(last_temps_by_tank):

    """this will withdraw data from redis and the function create_random_data_for_tanks
    without timestamp in one row, and compare each of the number in row with
    threshold temps"""

    thresh_check = namedtuple('thresh_check', ['tank','temp'])
    # now set a variable to empty that we can save the tuples in
    save_tuple_list = []
    for index, temp in enumerate(last_temps_by_tank):
        if temp <= 77: # temps in range dont save
            thresh_tuple = thresh_check(index, temp)
        elif temp >= 95:  # temps outside of range save
            thresh_tuple = thresh_check(index, temp)
        else: #if nothing then set the thresh_tuple to empty
            thresh_tuple = []
        if thresh_tuple:
            save_tuple_list.append(thresh_tuple)
    # is it better now??? are you there?
    return save_tuple_list


def out_of_range_email(tank_number):

    """if a temp is out of range we want to save the tank number and send it
    in an email"""
    # echo this will work with test_data.py
    sender = "alexlncl007@gmail.com"
    receiver = "alexlncl007@gmail.com" # maybe we need to put email here
    username = "alexlncl007@gmail.com"
    password = "laemXgp489on"
    message = "this tank is out of range %d" % tank_number
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.ehlo()
        print server, 'we make it here', username
        server.login(username, 'laemXgp489on')
        server.sendmail(sender, receiver, message)
        server.quit()
    except:
        print 'mail fails'


if __name__ == '__main__':
    data = 2
    out_of_range_email(data)
