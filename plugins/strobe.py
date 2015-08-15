#!/usr/bin/env python
import time
from color_utils import Color

# Super simple; when time mod cycle is zero, show input color.  Otherwise, show off_color.
class Strobe(object):
    def __init__(self, cycle=1, off_color=Color(0,0,0,0)):
        self.cycle = cycle/2.0
        self.off_color = off_color

    # This function retrieves the next color from the strobe object
    def next(self, color_in):
        # If we're ON
        if int(time.time()/self.cycle)%2 == 0:
            return color_in
        else:
            return self.off_color