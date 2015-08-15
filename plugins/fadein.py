#!/usr/bin/env python
import time
from math import exp
from color_utils import Color
from animation_utils import *

class Fadein(object):
	def __init__(self):
		self.t_start = time.time()
		self.last_t = self.t_start

		# Fade in over five seconds
		self.anim_queue = AnimationQueue()
		self.anim_queue.push(ease(0,1,5.0,sin_ease))

	# This function retrieves the next color from the startup object
	def next(self, color_in):
		# Fade in the input color
		return self.anim_queue.animate(default_value=1) * color_in