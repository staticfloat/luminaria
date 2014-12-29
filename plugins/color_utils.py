#!/usr/bin/env python
import colorsys

# A color object is just what it sounds like: it represents a single color in the RGB colorspace
# It provides operator overloading/functions for things like mixing between colors, scaling intensity,
# etc... Note that while a color object's r, g and b values may exceed 1.0 and fall below 0.0,
# when outputting to the LED light strip, the colors will be clamped to the [0, 1] range
class Color(object):
	def __init__(self, r=0, g=0, b=0):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	# Get/set color values in different color spaces
	def getRGB(self):
		return (self.r, self.g, self.b)

	def getHSV(self):
		return colorsys.rgb_to_hsv(self.r, self.g, self.b)

	def setRGB(self, r, g, b):
		self.r = float(r)
		self.g = float(g)
		self.b = float(b)

	def setHSV(self, h, s, v):
		rgb = colorsys.hsv_to_rgb(h,s,v)
		self.r = float(rgb[0])
		self.g = float(rgb[1])
		self.b = float(rgb[2])

	# Return a new color, mixing this color and the other color together linearly, where an amount of
	# 0 means completely the other color, and 1 means completely the self color.
	def mix(self, other, amnt):
		return amnt*self + (1 - amnt)*other





	###############################################################################################
	# OPERATOR OVERLOADING
	###############################################################################################

	# Test if two colors are equal to eachother (given a certain tolerance)
	def __eq__(self, other, tol=1e-7):
		return abs(self.r - other.r) < tol and abs(self.g - other.g) < tol and abs(self.b - other.b) < tol

	# Negate a color (useful only really for subtraction, etc...)
	def __neg__(self):
		return Color(-self.r, -self.g, -self.b)

	# Add two colors together
	def __add__(self, other):
		if type(other) is Color:
			return Color(self.r + other.r, self.g + other.g, self.b + other.b)
		if type(other) in (int, float):
			return Color( self.r + other, self.g + other, self.b + other)
		raise TypeError('unsupported operand type(s) for +: ' + type_as_str(self) + ' and ' + type_as_str(other))

	def __radd__(self, other):
		return self.__add__(other)

	# Subtract other from self
	def __sub__(self, other):
		return self.__add__(-other)

	# Subtract self from other
	def __rsub__(self, other):
		return (-self).__add__(other)

	def __mul__(self, other):
		if type(other) is Color:
			return Color( self.r * other.r, self.g * other.g, self.b * other.b)
		if type(other) in (int, float):
			return Color( self.r * other, self.g * other, self.b * other)
		raise TypeError('unsupported operand type(s) for *: ' + type_as_str(self) + ' and ' + type_as_str(other))

	def __rmul__(self, other):
		return self.__mul__(other)

	def __str__(self):
		return "Color object: (%.2f, %.2f, %.2f)"%(self.r, self.g, self.b)
	

