#!/usr/bin/python
#INTERFACING ADC MCP3008- Dibakar Barua
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

mosi = 19
miso = 21
sck = 23
cs = 7

GPIO.setup(mosi,GPIO.OUT)
GPIO.setup(miso,GPIO.IN)
GPIO.setup(sck,GPIO.OUT)
GPIO.setup(cs,GPIO.OUT)

def readadc (adcch):
	GPIO.output(cs, True)
	GPIO.output(sck, False) # start clock low
	GPIO.output(cs, False)	

	dataout = adcch
	# to set start bit and SGL bit and D2, D1, D0 as per adcch value
	dataout |= 0x18
	# only 5 control bits are needed 
	dataout <<= 3 
	for i in range(5):
		if ((dataout & 0x80) != 0):
			GPIO.output(mosi,True)
		else: 
			GPIO.output(mosi,False)
		dataout <<= 1
		GPIO.output(sck, True)
		GPIO.output(sck, False)	

	#initalize data to be read from adc
	datain = 0
	for i in range(12):
		GPIO.output(sck, True)
		GPIO.output(sck, False)
		datain <<= 1
		if(GPIO.input(miso)):
			datain |= 0x1
	
	GPIO.output(cs, True)
	#drop empty and null bits
	datain >>= 1 
	return datain

#main program
#infinite loop
while True:
	#read channel 0 and print value continuously
	adcval = readadc(0)
	print "adc value =" 	
	print(adcval)
	#give delay
	time.sleep(1)

	
