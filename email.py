#!/usr/bin/env python

from libled import LEDStrip
led = LEDStrip(rgb_channels=(12,13,14))
led.set_rgb(1.0, 1.0, 1.0)
import imaplib, time, sys

def linspace(start, stop, n):
    if n == 1:
        yield stop
        return
    start = 1.0*start
    stop  = 1.0*stop
    h = (stop - start) / (n - 1)
    for i in range(n):
        yield start + h * i

def blink(blink_duration=40):
    for i in linspace(1,.2,blink_duration/2):
        led.set_rgb(i,i,i)
        time.sleep(.01)
    for i in linspace(.2,1,blink_duration/2):
        led.set_rgb(i,i,i)
        time.sleep(.01)



M = imaplib.IMAP4_SSL('imap.gmail.com')

try:    
    M.login('staticfloat@gmail.com', 'kybimsjmy.google')
except imaplib.IMAP4.error:
    print 'LOGIN FAILED!!!'
    sys.exit()
    
# Look only in INBOX
M.select('INBOX')

last_unread_count = 0
while True:
    status, response = M.search(None, 'UNSEEN')
    unread_count = len(response[0].split())

    if last_unread_count != unread_count:
        if last_unread_count < unread_count:
            blink()
            time.sleep(.5)
            blink()
        last_unread_count = unread_count
    time.sleep(10)

M.logout()

