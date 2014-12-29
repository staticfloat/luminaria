#!/usr/bin/env python
import zmq, time, struct
from color_utils import Color
from animation_utils import *

# This guy listens for ZMQ packets on listen_port (defaults to 1337), and when he receives a packet,
# interprets the binary data as a floating point number, which is used to attenutate the incoming
# color.
#
# We also do fancy things when we don't receive any input data; after `timeout` seconds of not
# receiving any packets, we start to animate the 
class Audio(object):
	def __init__(self, listen_port=1337, timeout=4, timeout_fade_duration=4):
		# create a ZMQ context, a pair socket, and bind it to listen on socket 1337
		self.ctx = zmq.Context()
		self.socket = self.ctx.socket(zmq.PAIR)
		self.socket.bind("tcp://*:%d"%(listen_port))

		# Initialize variables
		self.power = 1
		self.timeout = timeout
		self.timeout_fade_duration = timeout_fade_duration

		# Setup our animation queue
		self.anim_queue = AnimationQueue()

		# The last time we got a message on our socket
		self.last_msg_time = time.time()

	# Close the socket and destroy the context if we're 
	def __del__(self):
		self.socket.close()
		self.ctx.destroy()

	# This function retrieves the next color from the Audio object
	def next(self, color_in):
		# Check to see if we have any packets
		if self.socket.poll(timeout=0):
			# Receive a single floating point number from the input data
			self.power = struct.unpack("!f", self.socket.recv())[0]

			# Keep track of the last time we got a message, and clear the animation queue
			self.last_msg_time = time.time()
			self.anim_queue.clear()
		else:
			# If we've not received a message for `timeout` seconds, slowly ease back to 1.0 power
			if self.last_msg_time + self.timeout < time.time() and self.power != 1.0:
				# Ease slowly from the current value of self.power to 1.0
				self.anim_queue.push(ease(self.power, 1.0, self.timeout_fade_duration, sin_ease))

				# This ensures that once the animation is done, we stay at 1.0, and also that we
				# don't keep on animating over and over again (e.g. the if statement directly above
				# doesn't keep on activating over and over again)
				self.power = 1.0

		# If we're easing back to 1.0 after a client disconnect, then this animation does something.
		# If we're receiving packets like normal, this animation does nothing
		animated_power = self.anim_queue.animate(default_value=self.power)
		return color_in * animated_power
