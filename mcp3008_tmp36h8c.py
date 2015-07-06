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

import spidev
import time
import os

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)

# Define a function to clear the screen between scans of the channels
def cls(): print "\n" * 100

# Loop for selected number of scans of channels
for loopx in range(20):
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
  #time.sleep(5)
  #adc = spi.xfer2([1,(8+channel)<<4,0])
  #outputdata = adc
  #convert the variable adc to a decimal value
  #data = ((adc[1]&3) << 8) + adc[2]

 sleepx =1

 channel = 0 
 outputstring1 = [1,(8+channel)<<4,0]
 time.sleep(sleepx)
 adc = spi.xfer2([1,(8+channel)<<4,0])
 outputdata = adc
 data0 = ((adc[1]&3) << 8) + adc[2]


 channel = 1
 outputstring2 = [1,(8+channel)<<4,0]
 time.sleep(sleepx)
 adc = spi.xfer2([1,(8+channel)<<4,0])
 outputdata = adc
 data1 = ((adc[1]&3) << 8) + adc[2]


 channel = 2
 outputstring3 = [1,(8+channel)<<4,0]
 time.sleep(sleepx)
 adc = spi.xfer2([1,(8+channel)<<4,0])
 outputdata = adc
 data2 = ((adc[1]&3) << 8) + adc[2]


 channel = 3
 outputstring4= [1,(8+channel)<<4,0]
 time.sleep(sleepx)
 adc = spi.xfer2([1,(8+channel)<<4,0])
 outputdata = adc
 data3 = ((adc[1]&3) << 8) + adc[2]



 print [(data1)/(1023/5)]


#  print channel , outputstring
#  outputstring0 is the string sent to the ADC to retrieve chip channel 0  this is done by the spi.xfer2 program

# the folowing prints out the loopx then the four channels outputs in decimal and then the four input strings that call the ADC's channels 0,1,2,3
 print [loopx,data0 ,data1,data2,data3],[outputstring1,outputstring2,outputstring3, outputstring4]
 print loopx,data0 ,(data1)/(1023/5),data2,data3

 print loopx,data0 ,"%.3f"%((data1)/(1023/5)),data2,data3

