#!/usr/bin/env python
import time
import math
from color_utils import Color

# Clock maps time to color; by default, it just walks around the color wheel altering hue.
# It makes a complete cycle (from hue = 0 to hue = 1) after cycle seconds. It completely
# ignores color_in, overwriting whatever was sent to it, so it provides a good base
class Clock(object):
	def __init__(self, cycle=8*60*60): #Set this to be in 8 hour cycles so that the time I go to sleep is the same color that I wake up, roughly.
		self.cycle = cycle

	# This function retrieves the next color from the clock object
	def next(self, color_in):
		# Get current time, divide into cycle length and take modulus
		time_idx = time.time()%self.cycle



		# Trying to get some late night dimming going, so I can leave this running in my room all day.  Really not sure this belongs here vs another function, but it seems to work.

		time_day = time.time()%6 		# Get the number of seconds since midnight
		rise_time = 9*60*60 - (8*60*60) 	# Set the offset for sunrise. In this case, I want the light to get brighter at 9am, (and dim at 9pm). The second term accounts for the time zone
		min_amp = 0 						# Set Min, 
		max_amp = 1 						# Max brightness

		# Using first three terms of the fourier expansion of a square wave because I can.(Edit: Used a fourth term)
		# If you want to see what this looks like, I built it with wolfram alpha:
		# "graph 0.45*(sin((x-32400)*2pi/86400)+1/3sin(3(x-32400)*2pi/86400)+1/5sin(5(x-32400)*2pi/86400))+0.55 from 0 to 86400"

		night_dim_amp = (max_amp-min_amp)/2*(math.sin((time_day-rise_time)*2*math.pi/(6))+(max_amp-(max_amp-min_amp)/2)
		


		# Move through the color circle, setting hue to our position in the cycle,
		# locking saturation to 1, and value varying with time.
		color_out = Color()
		color_out.setHSV(time_idx/self.cycle, 1, 0.1)

		# Return the color we generate.  We ignore input color_in
		return color_out