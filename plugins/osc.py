#!/usr/bin/env python
import time, struct, types
from color_utils import Color
from animation_utils import *
from OSC import OSCServer

# This guy listens for OSC packets on listen_port (defaults to 7331), and when he receives a packet,
# expects three floating point numbers, targeted at either the "/rgb" or "/hsv" endpoints. The color
# set by these values completely overrides color coming in from previous plugins.  When no packets
# have been received after `timeout` seconds, the output color fades back to the `color_in` over the
# course of `timeout_fade_duration` seconds.

class Osc(object):
	def __init__(self, listen_port=7331, timeout=4, timeout_fade_duration=4):
		# create an OSC server and bind it to listen on port 7331
		self.server = OSCServer( ("", listen_port) )
		self.server.timeout = 0
		self.server.handle_timeout = types.MethodType(lambda x: self.handle_timeout(), self.server)

		# Create handlers for "/rgb" and "/hsv".  This causes a packet to "/rgb" to call self.set_rgb()
		# and a packet to "/hsv" to call self.set_hsv(), with the arguments path, tags, args, source
		self.server.addMsgHandler( "/rgb", lambda p, t, a, s: self.set_rgb(p, t, a, s))
		self.server.addMsgHandler( "/r", lambda p, t, a, s: self.set_r(p, t, a, s))
		self.server.addMsgHandler( "/g", lambda p, t, a, s: self.set_g(p, t, a, s))
		self.server.addMsgHandler( "/b", lambda p, t, a, s: self.set_b(p, t, a, s))
		self.server.addMsgHandler( "/hsv", lambda p, t, a, s: self.set_hsv(p, t, a, s))
		self.server.addMsgHandler( "/h", lambda p, t, a, s: self.set_h(p, t, a, s))
		self.server.addMsgHandler( "/s", lambda p, t, a, s: self.set_s(p, t, a, s))
		self.server.addMsgHandler( "/v", lambda p, t, a, s: self.set_v(p, t, a, s))

		# Initialize variables
		self.color = Color(0.0, 0.0, 0.0)
		self.opacity = 0.0
		self.timeout = timeout
		self.timeout_fade_duration = timeout_fade_duration

		# Setup our animation queue
		self.anim_queue = AnimationQueue()

		# The last time we got a message on our socket
		self.last_msg_time = time.time()

	# Close the socket on exit
	def cleanup(self):
		self.server.close()

	def got_a_packet(self):
		self.opacity = 1.0
		self.last_msg_time = time.time()
		self.anim_queue.clear()


	# Set the current color in either RGB or HSV colorspace
	def set_rgb(self, path, tags, args, source):
		self.color.setRGB(*args)
		self.got_a_packet()

	def set_r(self, path, tags, args, source):
		print path, tags, args, source
		self.color.setR(args[0])
		self.got_a_packet()

	def set_g(self, path, tags, args, source):
		self.color.setG(args[0])
		self.got_a_packet()

	def set_b(self, path, tags, args, source):
		self.color.setB(args[0])
		self.got_a_packet()

		
	def set_hsv(self, path, tags, args, source):
		self.color.setHSV(*args)
		self.got_a_packet()

	def set_h(self, path, tags, args, source):
		self.color.setH(args[0])
		self.got_a_packet()

	def set_s(self, path, tags, args, source):
		self.color.setS(args[0])
		self.got_a_packet()

	def set_v(self, path, tags, args, source):
		self.color.setV(args[0])
		self.got_a_packet()


	# This gets called when we have no more packets waiting to be processed
	def handle_timeout(self):
		self.timed_out = True


	# This function retrieves the next color from the Audio object
	def next(self, color_in):
		# process any messages we might have waiting for us.  We do this by calling handle_request() until
		# handle_timeout() gets called, at which point we stop:
		self.timed_out = False
		while not self.timed_out:
			self.server.handle_request()
			
		# If we've not received a message for `timeout` seconds, slowly ease back to 1.0 power
		if self.last_msg_time + self.timeout < time.time() and self.opacity != 0.0:
			# Ease slowly from the current value of self.opacity to 0.0
			self.anim_queue.push(ease(self.opacity, 0.0, self.timeout_fade_duration, sin_ease))

			# This ensures that once the animation is done, we stay at 0.0, and also that we
			# don't keep on animating over and over again (e.g. the if statement directly above
			# doesn't keep on activating over and over again)
			self.opacity = 0.0

		# If we're easing back to 0.0 after a client disconnect, then this animation does something.
		# If we're receiving packets like normal, this animation does nothing, it just returns self.opacity
		animated_opacity = self.anim_queue.animate(default_value=self.opacity)

		# Mix between color_in and our stored self.color
		return color_in * (1.0 - animated_opacity) + animated_opacity * self.color
