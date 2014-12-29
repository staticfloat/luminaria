#!/usr/bin/env python

import time, sys, traceback, os
from libled import LEDStrip
from plugins.color_utils import Color
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
	# If we get any event that ends in .py that's not a directory, restart ourselves
	def on_any_event(self, event):
		if not event.is_directory and event.src_path[-3:] == '.py':
			print "Change detected in %s, restarting!"%(event.src_path)
			os.execv(__file__, sys.argv)

# Startup watchdog
obs = Observer()
event_handler = ReloadHandler()
obs.schedule(event_handler, ".", recursive=True)
obs.start()


# Initialize our LED strip
led = LEDStrip(rgb_channels=(12,13,14))

# Try to import plugin_config, if it fails, then blink angrily
try:
	import plugin_config
except Exception, err:
	# Print the actual syntax error
	print "ERROR LOADING PLUGIN CONFIGURATION:"
	print traceback.format_exc()

	# Something went horribly wrong, just strobe red now until we get fixed
	print "BLINKING ANGRILY UNTIL YOU FIX ME!!!"
	from plugins import strobe
	s = strobe.Strobe(cycle=1)
	while True:
		color = s.next(Color(1,0,0))
		led.set_color(color, quiet_fool=True)
		time.sleep(0.005)

last_color = None
while True:
	# Start with white
	color = Color(1, 1, 1)

	# Filter through all plugins, sequentially
	for plugin in plugin_config.plugin_objs:
		color = plugin.next(color)

	# Output final color, IFF this color is different than what we had last time!
	if last_color != color:
		led.set_color(color)
		last_color = color

	# Sleep for 5ms then DO IT AGAIN!!!!
	time.sleep(.005)
