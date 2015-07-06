# THIS SCRIPT TAKEN FROM SEVERAL SOURCES TO SCAN AN ADC
# CONVERTER CHIP AND DISPLAY THE DATA SENT BACK
# THE CHIP USES THE SPI PROTOCOL
# March 8, 2015
# Note that this script is for an MCP3008 ADC chip


#!/usr/bin/python
#--------------------------------------
# This script reads data from a
# MCP3008 ADC device using the SPI bus.
#
# Author : Matt Hawkins
# Date   : 13/10/2013
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------
#
# FURTHER MODIFICED FROM mcp3008_tmp36h8d2ba.py
# THIS VERSION ATTEMPTS TO WRITE TO OUTPUT.CSV WITH ACTUAL DATA FROM THE ADC CHIP
# 18 MAY 2015
# THE CURRENT FORMAT OF THAT FILE IS AS FOLLOWS
#           ZADD Temps 1431999601 "[64.6, 75.0, 60.3, 70.0, 75.1, 57.1, 73.3, 58.1, 1431999601]"

import spidev
import time
import os
import math







from datetime import datetime
datetime.now()
#datetime.datetime(2007, 3, 3, 22, 20, 11, 443849)
#print datetime.datetime
y = datetime.now()
print y
from datetime import datetime
datetime.now()
#datetime.datetime(2007, 3, 3, 22, 20, 11, 443849)
#print datetime.datetime
y = datetime.now()
print y






# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Define a function to clear the screen between scans of the channels
def cls():
    print "\n" * 100


# Loop for selected number of scans of channels




for loopx in range(20000):
    print loopx









       


 # Wait some time between scans to reduce CPU activity
#time.sleep(5)
 # Clear screen between scans of  channels
#cls()

# Scan the chip input channels
 #for channel in range(4):
  #the MCP3008 chip has 8 analog channels available
  #this program requests data from all 8 channels
  #the chip labels these from 0 to 7
  #the code (8+channel)<<4.0)  converts the decimal 'channel' number to binary value
       #of each channel, e.g. for channel 0, it outputs binary value of decimal 128
       #this is binary 10000000     The next channel is 1 and the output is
       #decimal 144 which is  binary 1001000

  #generate a string to send to the ADC chip that will send back one channel value
  #outputstring = [1,(8+channel)<<4,0]
       #note that the format of the string sent to the ADC chip is in [x,y,z]
       #where x=1 because the spidev needs it
       #where y=an eight bit binary value corresponding to the channel number
       #where z=0 because the spidev needs it
       #        further note-  the x and z relate to chip set up and would be a constant for a given hardware setup


  #send the 'outputstring' to the ADC chip using the function spi.xfer2 which
    #returns it to the variable adc
  #adc = spi.xfer2([1,(8+channel)<<4,0])


                                   #    time.sleep(1)
  #adc = spi.xfer2([1,(8+channel)<<4,0])
  #outputdata = adc
  #convert the variable adc to a decimal value
  #data = ((adc[1]&3) << 8) + adc[2]

   

    channel = 0
    outputstring1 = [1,(8+channel)<<4,0]
    
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data9 = ((adc[1]&3) << 8) + adc[2]
         
    time.sleep(2)   #was 10, was that better??
    channel = 0
    outputstring1 = [1,(8+channel)<<4,0]

    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data0 = ((adc[1]&3) << 8) + adc[2]

    channel = 1
    outputstring2 = [1,(8+channel)<<4,0]
    
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data1 = ((adc[1]&3) << 8) + adc[2]

    channel = 2
    outputstring3 = [1,(8+channel)<<4,0]
    
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data2 = ((adc[1]&3) << 8) + adc[2]


    channel = 3
    outputstring4= [1,(8+channel)<<4,0]
    
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data3 = ((adc[1]&3) << 8) + adc[2]



    channel = 4
    outputstring4= [1,(8+channel)<<4,0]
   
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data4 = ((adc[1]&3) << 8) + adc[2]



    channel = 5
    outputstring4= [1,(8+channel)<<4,0]
    
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data5 = ((adc[1]&3) << 8) + adc[2]


    channel = 6
    outputstring4= [1,(8+channel)<<4,0]
   
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data6 = ((adc[1]&3) << 8) + adc[2]



    channel = 7
    outputstring4= [1,(8+channel)<<4,0]
    
    adc = spi.xfer2([1,(8+channel)<<4,0])
    outputdata = adc
    data7 = ((adc[1]&3) << 8) + adc[2]


    y=datetime.now()

#  print channel , outputstring
#  outputstring0 is the string sent to the ADC to retrieve chip channel 0  this is done by the spi.xfer2 program

# the folowing prints out the loopx then the four channels outputs in decimal
# and then the four input strings that call the ADC's channels 0,1,2,3
    print [data0,data1,data2,data3,data4,data5,data6, data7]


    # following three variables are for relating the ADC readings to external measusrment
    #                (in this case, temperature)
    # the three constants a, b, c are the factors in a second order polynomial that were 
    #                 determined by placing the thermistors in known temperatures and reading the data
    #                 reported by this Python program  (a separate document illustrates the process)
    # for the purposes of this demo project, the three thermistors are deemed to have the same set of constants
    #                 In fact, the error due to this convienience is rather negligable, roughly 10% or less
    # Note that the polynomial seems reverse, that is higher temperature shows lower readings.  This is due
    #                 to the fact that the thermistors, as wired to the ADC chip, have that fundamental physical 
    #                 properties.  This is illustrated in a separate document on Properties Of Thermistors

    # (side bar issue) the following constants are given type floating point by setting them with floating point value
                      # not sure if this is correct in Python but it seems to work
                      # for this reason, in each print group below, datax is made floating by adding a tiny amount, .0001 which is, of course, a floating point constant and has no signficant effect on the result

    a=-40.36
    b= 283.0
    c= 1.0   # not used

    vcc = 5.09  # actual measured 'reference' voltage of ADC


    # the following takes the data for each channel, one by one, and calculates with the polynomial the program
                      # value for temperature and prints it to the screen so that it can be compared to the 
                      # actual temperature at the test water barrel in three places, ambient temp (chan0), 
                      # barrel outside wall (chan1), and water in barrel (chan2)   
    
    print "chan0",
    print data0,
   # print str(data0)
    datax = data0 + .0001
    #print datax
    #print datax + .2
    # the following calculates the voltage of the given channel since 10 bits is (ACD chip)  maximum value and is decimal 1023
    # so the ADC value is divided by the full scale value of 1023.  This is the fraction of full scale. 
    #     For this project, the full scale value is 5.0 volts dc
    print (datax / 1023.0)*vcc,
    # the following calculates and prints the temperature of the sensor environment.  For example chan0 value is data0
    #       this is done according to a polynomial using the coefficients given above: a,b,c
    #       the formula is based on readings in degrees C as measured during a calibration
    c=math.log(datax)
    d= ((a*c) + b)
    d0=d
    print d




    print "chan1",
    print data1,
   # print str(data0)
    datax = data1 + .00001
    #print datax
    #print datax + .2
    print (datax / 1023.0)*vcc,
    c=math.log(datax)
    d= ((a*c) + b)
    d1=d
    print d



    print "chan2",
    print data2,
   # print str(data0)
    datax = data2 + .1
    #print datax
    #print datax + .2
    print (datax / 1023.0)*vcc,
    c=math.log(datax)
    d= ((a*c) + b)
    d2=d
    print d




    print "chan3",
    print data3,
   # print str(data0)
    datax = data3 + .1
    #print datax
    #print datax + .2
    print (datax / 1023.0)*vcc,
    c=math.log(datax)
    d= ((a*c) + b)
    d3=d
    print d


    
    print "chan4",
    print data4,
   # print str(data0)
    datax = data4 + .1
    #print datax
    #print datax + .2
    print (datax / 1023.0)*vcc,
    c=math.log(datax)
    d= ((a*c) + b)
    d4=d
    print d


    print data9
    print vcc

    # exit()

    #print "%.1f" % d0,"%.1f" % d1,"%.1f" % d2,"%.1f" % d3,"%.1f" % d4;
    #output only the three current active sensors:  tank air, tank outer surface, tank water  REPEATE THESES to make up to 8 channels
  #  print "ZADD Temps 1234567890",  ""\[", "%.1f" % d0,"%.1f" % d1,"%.1f" % d2,"%.1f" % d0,"%.1f" % d1, "%.1f" % d2, "%.1f" % d0, "%.1f" % d1, "1234567890 ]" ;
   #  print "%.2f" % d0, "12345\"",  "\"";

    epochtimenow = str( "%.f" % time.time())
    print epochtimenow


    print "ZADD Temps " + epochtimenow ,  '"' + "[" , 
    print "\b" + str("%.1f" % d0)+ ","  , str("%.1f" % d1)+ ","  , str("%.1f" % d2)+ ","   ,
    print str("%.1f" % d0)+ ","  , str("%.1f" % d1)+ ","  , str("%.1f" % d2)+ ","   ,
    print str("%.1f" % d0)+ ","  , str("%.1f" % d1)+ ", "  + epochtimenow ,
    #print "1234567890" ,
    print "\b]" + '"' ;
    
    #print "Item \"" + "Name" + "\" "
    #exit()



    line1 =  "ZADD Temps " + epochtimenow +  ' "' + "["  
    line2 = ( str("%.1f" % d0)+ ", "   + str("%.1f" % d1)+ ", "  +  str("%.1f" % d2)+ ", "    )
    #line2 = ( "\b" + str("%.1f" % d0)+ ", "   + str("%.1f" % d1)+ ", "  +  str("%.1f" % d2)+ ", "    )
    line3 = ( str("%.1f" % d0)+ ", "  + str("%.1f" % d1)+ ", "  + str("%.1f" % d2)+ ", "   )
    line4 = ( str("%.1f" % d0)+ ", "  + str("%.1f" % d1)+ ", "  + epochtimenow  )
    #print "1234567890" ,
    line5 = ( "]" + '"' )
    # line5 = ( "\b]" + '"' )
    line6 = "\n"

    f=open ("Output.txt","a")
    f.write(line1)
    f.write(line2)
    f.write(line3)
    f.write(line4)
    f.write(line5)
    f.write(line6)
    
    f.close


    f=open ("charactertest.txt","a")
    f.write('''1234567890-=!@$%^&*()_+QWERTYUIOP{}|[]\kl;'KL:   ,  /M<>/M<>?''')
    f.close



    exit()







    print data1
    print str(data1)
    datax = data1 + .1
    print datax
    print datax + .2
    print (datax / 1023)*5.0
    print 





    print data2
    print str(data2)
    datax = data2 + .1
    print datax
    print datax + .2
    print (datax / 1023.0)/5


    print data3
    print str(data3)
    datax = data3 + .1
    print datax
    print datax + .2
    print (datax / 1023)*5.0




    print data4
    print str(data4)
    datax = data4 + .1
    print datax
    print datax + .2
    print (datax / 1023)*5.0


#THIS SECTION WAS CREATED TO WRITE TO A FILE FOR CONVIENIENCE OF RECORDING ACTUAL DATA IN A FILE

    f=open ("test3a.txt","a")
   

    f.write(" * ")
    


    f.write(str(loopx))
    f.write(" % ")
    f.write(" , ")

    f.write(str(data0))
    f.write(" , ")

    
    f.write(str(data1))
    f.write(" , ")


    f.write(str(data2))
    f.write(" , ")
    
    f.write(str(data3))
    f.write(" , ")

    f.write(str(data4))
    f.write(" , ")
    

    f.write(str(data5))
    f.write(" , ") 


    f.write(str(data6))
    f.write(" , ")
   
    f.write(str(data7))
    f.write(" , ")
    f.write(" $ ")
    f.write(" , ")

    f.write(str(y))
    f.write(" , ")

    f.write(" & ")

    f.write("\n")










    f.close
#    for loopy in range(100100):
 #       print loopy
    #NOW GENERATE A STRING THAT CONTAINS ACTUAL CHANNEL DATA IN DEG C 
    #NOTE THAT THERE ARE ONLY FOUR CHANNELS ACTIVES SO FOR THIS TEST THE VALUES WILL BE REPEATED

    print d0,d1,d2,d3,d4;"asdf"

