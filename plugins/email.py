#!/usr/bin/env python

import imaplib, time
from color_utils import Color
from animation_utils import *

# Check for email once every 5 seconds, if we find a new message that wasn't in the unread list before,
# drop the color toward black twice "blinking" the color.
#
# Constructor Parameters:
#       username: Your gmail address
#       password: cleartext password to login over IMAP
# blink_duration: The duration of time it takes for the attenuation to go from 1 -> 0 -> 1
#     blink_skew: Portion of time spent during the dimming part of the blink, rather than the brightening
#                 (Default of 0.5 == equal time spent, 0.25 == 1 -> 0 is one-third the length of 0 -> 1)
#     interpause: Amount of time between the two blinks in seconds
# check_interval: Amount of time between new email checks in seconds

class Email(object):
    def __init__(self, username, password, blink_duration=.5, blink_skew=.5, interpause=1, check_interval=5):
        self.username = username
        self.password = password
        self.blink_duration = blink_duration
        self.blink_skew = blink_skew
        self.interpause = interpause
        self.check_interval = check_interval

        # Create our internal animation queue for blinking and such
        self.anim_queue = AnimationQueue()
        self.attenuation = 1.0

        # We delay logging in over IMAP since it freezes up the pi for a bit, and we like
        # our awesomely smooth intro animation.
        self.imap = None

        # Store the last time we checked for unread messages (Don't check for the first 10 seconds)
        self.last_check = time.time() + 10
        


    # Returns a list of unread message IDs
    def get_unread(self):
        status, response = self.imap.search(None, 'unseen')
        return response[0].split()

    # This function retrieves the next color from the Email object
    def next(self, color_in):
        curr_time = time.time()
        
        # If we haven't checked recently, then let's check to see if we have a new email:
        if curr_time > self.last_check + self.check_interval:
            # If we've never logged in before, do that here over IMAP
            if self.imap == None:
                self.imap = imaplib.IMAP4_SSL('imap.gmail.com')
                self.imap.login(self.username, self.password)
                self.imap.select('inbox')
                self.last_unread = self.get_unread()
                self.last_check = curr_time
            else:
                # Otherwise, let's check for messages
                self.last_check = curr_time
                unread = self.get_unread()

                # If any of the messages that are currently unread were not unread last check, then
                # queue up the animations to do a double-blink, using blink_duration and interpause
                if any([z for z in unread if not z in self.last_unread]):
                    # First, queue up a 1 -> 0 and 0 -> 1 easing, using sin easing
                    self.anim_queue.push(ease(1, 0, self.blink_skew*self.blink_duration/2, sin_ease))
                    self.anim_queue.push(ease(0, 1, (1 - self.blink_skew)*self.blink_duration/2, sin_ease))

                    # Then queue up a 1 -> 1 easing using linear easing (this is the interpause)
                    self.anim_queue.push(ease(1, 1, self.interpause))

                    # Finally, bounce 1 -> 0 -> 1 again:
                    self.anim_queue.push(ease(1, 0, self.blink_skew*self.blink_duration/2, sin_ease))
                    self.anim_queue.push(ease(0, 1, (1 - self.blink_skew)*self.blink_duration/2, sin_ease))

                # Remember to set the last unread here!
                self.last_unread = unread

        # Animate the attenuation if we're blinking
        animated_attenuation = self.anim_queue.animate(default_value=self.attenuation)
        
        # Use animated attenuation to attenuate color_in
        return color_in * animated_attenuation
