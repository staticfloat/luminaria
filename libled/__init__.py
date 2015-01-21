#!/usr/bin/env python

# This file interfaces with the Adafruit PWM servo driver library, allowing us to 
# control our sweet, sweet RGB LED lights!

try:
	from Adafruit_PWM_Servo_Driver import PWM

	class LEDStrip(object):
		# Initialize internal PWM object,
		def __init__(self, i2c_addr=0x40, rgb_channels=(1,2,3), pwm_freq=1600):
			self.r_channel = rgb_channels[0]
			self.g_channel = rgb_channels[1]
			self.b_channel = rgb_channels[2]
			self.pwm = PWM(i2c_addr)
			self.pwm.setPWMFreq(pwm_freq)
			self.last_values = {self.r_channel:None, self.g_channel:None, self.b_channel:None}
			self.set_rgb(0,0,0)

		# Gotta clamp to [0, 1], then translate to 12-bit PWM number
		def floatmap(self, intensity):
			intensity = max(0.0, min(1.0, intensity))
			int_tensity = int(4094*(1.0 - intensity) + 1)
			return int_tensity

		# Given a channel number and an intensity in [0.0, 1.0], send the appropriate PWM command
		# Only actually send the command if we're changing the int_tensity to avoid flicker
		def set_channel(self, channel_num, intensity):
			int_tensity = self.floatmap(intensity)
			if int_tensity != self.last_values[channel_num]:
				self.pwm.setPWM(channel_num, int_tensity, 0)
				self.last_values[channel_num] = int_tensity

		def set_rgb(self, r, g, b, quiet_fool=False):
			self.set_channel(self.r_channel, r)
			self.set_channel(self.g_channel, g)
			self.set_channel(self.b_channel, b)

		def set_color(self, color, quiet_fool=False):
			self.set_channel(self.r_channel, color.r)
			self.set_channel(self.g_channel, color.g)
			self.set_channel(self.b_channel, color.b)
except:
	print "Unable to load PWM driver; defining dummy interface that just prints RGB values for testing"
	class LEDStrip(object):
		def __init__(self, i2c_addr=0x40, rgb_channels=(1,2,3), pwm_freq=1600):
			pass
		
		def set_rgb(self, r, g, b, quiet_fool=False):
			if not quiet_fool:
				print "Direct RGB: (%.2f, %.2f, %.2f)"%(r,g,b)

		def set_color(self, color, quiet_fool=False):
			if not quiet_fool:
				print color
