import os, sys

# This file does some magic so that when you say `from plugins import *` there is a variable called
# pluginList that maps strings to actual plugin classes.  So you can do things like say:
#
#   pluginList['clock']
#
# and it will return the class plugins.clock.Clock.  This allows you to do things like:
#
#   x = pluginList['clock']()
#
# to construct a Clock object with default arguments, and assign it to the variable `x`.

pluginList = {}

for module_file in os.listdir(os.path.dirname(__file__)):
    if module_file == '__init__.py' or module_file[-3:] != '.py':
        continue

    modname = module_file[:-3]
    module = __import__(modname, locals(), globals())

    if hasattr(module, modname.title()):
    	pluginList[modname] = getattr( module, modname.title())
del module_file