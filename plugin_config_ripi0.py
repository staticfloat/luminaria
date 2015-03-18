#!/usr/bin/env python
from plugins import pluginList

## This is where you define what plugins you want to run, and how you want to daisy-chain them.
## You construct plugin objects from pluginList, and add them to the list plugin_objs. We will
## initialize it to be an empty list, and will add items to it using plugin_objs.append()

plugin_objs = []

# Simplest example: clock. This guy takes in one parameter, the cycle time period.  We will use
# the default value, take a look inside plugins/clock.py to find the default cycle value.
clock = pluginList['clock'](cycle=12*60*60)
plugin_objs.append(clock)

# Slighly more complicated example: strobe.  This guy takes in two parameter, the cycle duration
# in seconds and the color to change to when the strobe is "off", which we pass in to show how to
# pass in parameters.  We use the name not because it's necessary, but so that you get used to that
# since we'll use that syntax a lot, especially when we provide certain parameters but not others
# I'm commenting it out for now, but feel free to comment it in to give yourself a stroke

#strobe = pluginList['strobe'](cycle=.3, off_color=(0,0,0))
#plugin_objs.append(strobe)


# Even more complicated example: email.  This guy has two required parameters: username/password
# We'll pass those in, along with two optional parameters, blink_duration and interpause:
#email = pluginList['email'](
#	username="staticfloat@gmail.com",
#	password="xxxxxxxxxxxxx",
#	blink_duration=4.0,
#	blink_skew=.1,
#	interpause=0
#)
#plugin_objs.append(email)

# Lastly, the big one.  Audio.  No options.  This guy's way too cool for that.
#audio = pluginList['audio']()
#plugin_objs.append(audio)

#audiomassacre = pluginList['audiomassacre']

osc = pluginList['osc']()
plugin_objs.append(osc)

# We put the super-awesome startup plugin at the end so that it takes complete control during startup.  >:D
startup = pluginList['startup']()
plugin_objs.append(startup)
