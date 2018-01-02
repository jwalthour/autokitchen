#!/usr/bin/env python

"""

This application runs an automated roast profile.
See farther down for assumptions about pins.

"""
import time, math
import RPi.GPIO as GPIO

from sensors.max31865 import max31865

# Pin assignments

# High to enable heating element, low to disable.
PIN_HEATER_ON = 4

# SPI 0 - connection to MAX31865 PTC amplifier
PIN_THERMISTOR_CS   = 8
PIN_THERMISTOR_MISO = 9
PIN_THERMISTOR_MOSI = 10
PIN_THERMISTOR_CLK  = 11

# For early demos, use bang-bang control with hardcoded setpoints.
# SETPOINT_HIGH_C = 220.0
# SETPOINT_LOW__C = 210.0
SETPOINT_HIGH_C = 70.0
SETPOINT_LOW__C = 50.0

def c_to_f(c_temp):
	return c_temp * 9.0/5.0 + 32.0

if __name__ == "__main__":
	# Initialize IO
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	thermistor = max31865(PIN_THERMISTOR_CS  ,
							PIN_THERMISTOR_MISO,
							PIN_THERMISTOR_MOSI,
							PIN_THERMISTOR_CLK )
	thermistor.setCal(95.104980, 127.539062)
	GPIO.setup(PIN_HEATER_ON, GPIO.OUT)
	GPIO.output(PIN_HEATER_ON, GPIO.LOW)
	
	print("Will use bang-bang control loop to seek %f-%f degrees C."%(SETPOINT_HIGH_C, SETPOINT_LOW__C))
	raw_input("Turn on fan and press enter.")
	
	turnHeaterOn = False
	
	try:
		while True:
			tempC = thermistor.readTemp()
			
			if tempC > SETPOINT_HIGH_C:
				turnHeaterOn = False
			elif tempC < SETPOINT_LOW__C:
				turnHeaterOn = True
			else:
				pass # We're between the two setpoints; leave it at whatever it was last iteration
			
			print("Temp is %f degrees C (%f F).  Heater: %r"%(tempC, c_to_f(tempC), turnHeaterOn))
			if turnHeaterOn:
				GPIO.output(PIN_HEATER_ON, GPIO.HIGH)
			else:
				GPIO.output(PIN_HEATER_ON, GPIO.LOW)
	finally:
		GPIO.output(PIN_HEATER_ON, GPIO.LOW)
		GPIO.cleanup()
		