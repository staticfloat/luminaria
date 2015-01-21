#!/usr/bin/env python
from plugins import pluginList


plugin_objs = []

clock = pluginList['clock'](cycle=3600)
plugin_objs.append(clock)

# Even more complicated example: email.  This guy has two required parameters: username/password
# We'll pass those in, along with two optional parameters, blink_duration and interpause:
email = pluginList['email'](
	username="staticfloat@gmail.com",
	password="kybimsjmy.google",
	blink_duration=4.0,
	blink_skew=.1,
	interpause=0
)
plugin_objs.append(email)

# Lastly, the big one.  Audio.  No options.  This guy's way too cool for that.
audio = pluginList['audio']()
plugin_objs.append(audio)

osc = pluginList['osc']()
plugin_objs.append(osc)

# We put the super-awesome startup plugin at the end so that it takes complete control during startup.  >:D
startup = pluginList['startup']()
plugin_objs.append(startup)
