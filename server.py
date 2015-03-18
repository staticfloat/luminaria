#!/usr/bin/env python

import time, sys, traceback, os
from libled import LEDStrip
from plugins.color_utils import Color
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ReloadHandler(FileSystemEventHandler):
	# If we get any event that ends in .py that's not a directory, restart ourselves
	def on_any_event(self, event):
		if not event.is_directory and event.src_path[-3:] == '.py' and not "record_client" in event.src_path:
			print "Change detected in %s, restarting!"%(event.src_path)
			try:
				for plugin in plugin_config.plugin_objs:
					try:
						plugin.cleanup()
					except:
						pass
			except:
				pass
			os.execv(__file__, sys.argv)

# Startup watchdog
obs = Observer()
event_handler = ReloadHandler()
obs.schedule(event_handler, ".", recursive=True)
obs.start()

# Initialize our LED strip
led = LEDStrip(rgbw_channels=(12,13,14,15))




# This is the function we call to say that we've hit a critical error
def error_blink():
	# Something went horribly wrong, just strobe red now until we get fixed
	print "BLINKING ANGRILY UNTIL YOU FIX ME!!!"
	from plugins import strobe
	s = strobe.Strobe(cycle=1)
	while True:
		color = s.next(Color(1,0,0,0))
		led.set_color(color, quiet_fool=True)
		time.sleep(0.005)




# Try to import plugin_config, if it fails, then blink angrily.  Note that 
plugin_config = None
try:
	import socket
	plugin_config = __import__("plugin_config_"+socket.gethostname(), locals(), globals())
except Exception, err:
	# Print the actual error location
	print "ERROR LOADING PLUGIN CONFIGURATION:"
	print traceback.format_exc()
	error_blink()



# Run loop, feeding plugins and such
try:
	while True:
		# Start with white
		color = Color(1, 1, 1, 0)

		# Filter through all plugins, sequentially
		for plugin in plugin_config.plugin_objs:
			color = plugin.next(color)

		# Output final color, IFF this color is different than what we had last time!
		led.set_color(color)

		# Sleep for 1ms then DO IT AGAIN!!!!
		time.sleep(.001)

except KeyboardInterrupt:
	# Explicitly do nothing when we hit CTRL-C
	pass
except:
	# When it wasn't a keyboard interrupt, blink angrily!!!
	print "ERROR DURING NORMAL EXECUTION:"
	print traceback.format_exc()
	error_blink()
