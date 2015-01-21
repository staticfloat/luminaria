#!/usr/bin/env python
import time, math

# Animation utilies allow you to create generators that interpolate values from a starting point to an
# ending point, for instance, interpolating 0 to .5 over the course of two seconds linearly:
#
#    obj = ease(0, .5, 2)
#
# Or interpolation from 0 to 10 over one second using sin easing:
#
#    obj = ease(0, 10, 1, sin_ease)
#
# Generator objects are objects that run code when you try to pull a value out of them.  You can think
# of them as functions that can return multiple times, (each you time call `yield`) and pick up from where
# they left off when you ask for the next value.  For instance, to get values out of the above objects,
# you could write a "for in" loop, sleeping 1/10th of a second in between:
#
#    for val in ease(0, .5, 2):
#        print val
#        sleep(0.1)
#
# Note that I don't explicitly tell the for loop how many values we're going to loop over, that is all
# calculated dynamically by animate(); it either yields a value, or it doesn't.  If it yields a value,
# it gets assigned to `val` and we execute the body of the for loop.  If it doesn't yield a value, 
# (e.g. it returns) the for loop ends.  Therefore, inside of `animate()` we check to see if the current
# time exceeds that of the duration of the animation, and if it has, we exit out of the funciton, thereby
# breaking the for loop.


# Given start value, end value, time duration, and time into animation cycle, return the interpolated value
def linear_ease(start, end, duration, t): 
	return start + (end - start)*t/duration

# The same as for linear above, but do sinusoidal easing rather than linear easing
def sin_ease(start, end, duration, t):
	return start + (end - start)*(.5 - .5*math.sin(math.pi/2 + math.pi*t/duration))


# Actual function you would call to perform easing.
def ease(start, end, duration, easing=linear_ease):
	t_start = time.time()
	t_end = t_start + duration
	curr_time = t_start		
	while curr_time < t_end:
		# Clamp to t_end so that we don't accidentally go past end
		curr_time = min(time.time(), t_end)

		# Call the actual easing function
		yield easing( start, end, duration, curr_time - t_start)



# This class represents a queue of animations that you can add on to in order to create a series of easings
# Used, for example, to create the double-blink in the Email plugin, as well as the fade to back to normal
# in the Audio plugin after a client disconnects
class AnimationQueue(object):
	def __init__(self):
		self.queue = []

	# Push a new animation onto the end of the list
	def push(self, animation):
		self.queue.append(animation)

	def pop(self, idx):
		self.queue.pop(idx)

	def clear(self):
		self.queue = []

	# Run the animation at the head of the queue, if it's finished, run the next, and so on until we run
	# out of things to run, at which point return default_value as a fallback
	def animate(self, default_value):
		while len(self.queue) > 0:
			try:
				# Try to return the next element from the current generators
				return next(self.queue[0])
			except StopIteration:
				# If we throw an error while trying to get the next value from this generator, throw out 
				# the current head of the queue, and try to move on to further animations
				self.queue.pop(0)
		
		# If we're fresh out of animations, return default_value
		return default_value


