#!/usr/bin/env python
#DIBAKAR BARUA- Interfacing I2C based light sensor
import smbus
import time
from math import floor
from math import pow
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False) #turn off warning statements

#check bus line and dev address first
bus = smbus.SMBus(1)

#macros in char form 
cmdreg = 0b10100000 
addrwrite = 0b01010010
addrread = 0b01010011
addrch0low = 0b10101100
addrch0high = 0b10101101
addrch1low = 0b10101110
addrch1high = 0b10101111

#dev address
address = 0b00101001

#i2c write command using library

def i2cwrite(txval):
	bus.write_byte(address, txval)

#i2c read command using library
def i2cread():
	value = bus.read_byte(address)
	return value
	
def lux_calc(CH1, CH0):
	k = CH1/CH0
	
	if((k>=0) & (k<=0.52)):
		Lux=(0.0315*CH0)-(0.0593*CH0*pow(k,1.4))
	elif((k>0.52) & (k<=0.65)):
		Lux=(0.0229*CH0)-(0.0291*CH1)
	elif((k>0.65) & (k<=0.80)):
		Lux=(0.0157*CH0)-(0.0180*CH1)
	elif((k>0.80) & (k<=1.30)):
		Lux=(0.00338*CH0)-(0.00260*CH1)
	else: 
		Lux=0
	return Lux

def APDS_init():
	i2cwrite(addrwrite) #device address + write bar bit (asperdatasheet)
	i2cwrite(cmdreg) #access cmd reg
	i2cwrite(0b00000011) #power up command
	time.sleep(0.001)

def APDS_read():
	Lux = 0
	i2cwrite(addrwrite) #address + write bar bit
	i2cwrite(addrch0low) #CH0 low byte register address
	time.sleep(0.001) #delay to accomodate ACK bit
	i2cwrite(addrread)
	ch0low = i2cread() #read the register and store value
	time.sleep(0.001)
	i2cwrite(addrwrite)
	i2cwrite(addrch0high) #CH0 high byte register address
	time.sleep(0.001)
	i2cwrite(addrread)
	ch0high = i2cread()
	time.sleep(0.001)
	i2cwrite(addrwrite)
	i2cwrite(addrch1low) #CH1 low byte register address
	time.sleep(0.001)
	i2cwrite(addrread)
	ch1low = i2cread()
	time.sleep(0.001)
	i2cwrite(addrwrite)
	i2cwrite(addrch1high) #CH1 high byte register address
	time.sleep(0.001)
	i2cwrite(addrread)
	ch1high = i2cread()
	time.sleep(0.002)
	CH0 = (ch0high << 8) | (ch0low) #pack high byte and low byte as 16 bit sensor value
	CH1 = (ch1high << 8) | (ch1low)
	Lux = lux_calc(CH1,CH0) #calculate luminosity
	return Lux

#main part of the program infinite loop
while True:
	print(time.time())
	APDS_init()
	print 'reading sensors'
	#timestamp
	luxval = APDS_read()
	print 'Lux Val is:'
       	print(luxval)
	



	
