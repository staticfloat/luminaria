#!/usr/bin/env python

from libled import LEDStrip
import colorsys, time, sys

led = LEDStrip(rgb_channels=(12,13,14))

# The number of seconds it takes to run through the full color circle
TIME_CYCLE = 2 # 60*60*4

# Run forever, sleeping for 1/10000th of TIME_CYCLE, or 1ms, whichever is more
sleep_time = max(TIME_CYCLE/10000.0, .001)
while True:
	# Get current time, divide into cycle length and take modulus
	time_idx = time.time()%TIME_CYCLE

	# Move through the color circle by TIME_CYCLE
	r, g, b = colorsys.hsv_to_rgb(time_idx/TIME_CYCLE, 1, 1)

	# Set the LEDs then sleep!
	led.set_rgb(r, g, b)
	time.sleep(sleep_time)
