#!/usr/bin/env python
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

		def floatmap(self, intensity):
			intensity = max(0.0, min(1.0, intensity))
			int_tensity = int(4094*(1.0 - intensity) + 1)
			return int_tensity

		# Given a channel number and an intensity in [0.0, 1.0], send the appropriate PWM command
		def set_channel(self, channel_num, intensity):
			self.pwm.setPWM(channel_num, self.floatmap(intensity), 0)

		def set_rgb(self, r, g, b):
			self.set_channel(self.r_channel, r)
			self.set_channel(self.g_channel, g)
			self.set_channel(self.b_channel, b)
except:
	print "Unable to load PWM driver; defining dummy LEDStrip class for testing"

	class LEDStrip(object):
		# Initialize internal PWM object,
		def __init__(self, i2c_addr=0x40, rgb_channels=(1,2,3), pwm_freq=1600):
			pass
			
		def set_rgb(self, r, g, b):
			print "(%.2f, %.2f, %.2f)"%(r,g,b)

