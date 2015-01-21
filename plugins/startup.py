#!/usr/bin/env python
import time
from math import exp
from color_utils import Color
from animation_utils import *

# This startup sequence begins by running around the color wheel 

class Startup(object):
	def __init__(self):
		self.t_start = time.time()
		self.last_t = self.t_start
		self.hue = 0

		# Setup an animation to ease from a mixing value of 1 to 0 over 2.0 seconds
		self.anim_queue = AnimationQueue()
		self.anim_queue.push(ease(1,0,5.0,sin_ease))
		self.white = Color(1,1,1)

	# This function retrieves the next color from the startup object
	def next(self, color_in):
		# Calculate both wallclock time since start, as well as time since last call of next()
		t = time.time() - self.t_start
		dt = t - self.last_t
		self.last_t = t

		if t < 6:
			# Val fades us in from black at the beginning, we use sin_ease to bring us in
			# We clamp to 1.0 since we're going to be running this well past the end time of .5
			# We're kind of abusing this function, it's meant to only be called from within ease()
			# but don't worry, we "Know What We're Doing" (TM)
			val = sin_ease(0, 1, 2.0, min(t, 2.0))

			# Color cycle continually accelerates
			self.hue_cycle = .7*exp(-.45*t)

			# Calculate new hue, modulo 1.0
			self.hue = (self.hue + dt/self.hue_cycle)%1.0

			# Have it saturate out to white from 3 seconds onward:
			sat = sin_ease(1, 0, 3.0, min(max(t - 3.0, 0.0), 3.0))

			# Calculate final color out
			color_out = Color()
			color_out.setHSV(self.hue, sat, val)
			return color_out

		# Once we're done with startup, ease from the ending white to our color:
		mix_amnt = self.anim_queue.animate(default_value=0)
		return mix_amnt * self.white + (1 - mix_amnt)*color_in