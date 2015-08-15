#!/usr/bin/env python
from plugins import pluginList


plugin_objs = []

clock = pluginList['clock'](cycle=3600)
plugin_objs.append(clock)

# Lastly, the big one.  Audio.  No options.  This guy's way too cool for that.
audio = pluginList['audio']()
plugin_objs.append(audio)

osc = pluginList['osc']()
plugin_objs.append(osc)

# We put the super-awesome startup plugin at the end so that it takes complete control during startup.  >:D
fadein = pluginList['fadein']()
plugin_objs.append(fadein)
