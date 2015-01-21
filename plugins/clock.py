#!/usr/bin/env python
import time
from color_utils import Color

# Clock maps time to color; by default, it just walks around the color wheel altering hue.
# It makes a complete cycle (from hue = 0 to hue = 1) after cycle seconds. It completely
# ignores color_in, overwriting whatever was sent to it, so it provides a good base
class Clock(object):
	def __init__(self, cycle=24*60*60):
		self.cycle = cycle

	# This function retrieves the next color from the clock object
	def next(self, color_in):
		# Get current time, divide into cycle length and take modulus
		time_idx = time.time()%self.cycle

		# Move through the color circle, setting hue to our position in the cycle,
		# locking saturation to 1, and value to 0.25 (this will help with overheating while lights are coiled)
		color_out = Color()
		color_out.setHSV(time_idx/self.cycle, 1, 0.25)

		# Return the color we generate.  We ignore input color_in
		return color_out