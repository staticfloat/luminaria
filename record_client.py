#!/usr/bin/env python
import pyaudio, struct, zmq, sys
from numpy import *

# In order to run this puppy you need to:
# 
# brew install portaudio
# easy_install pyaudio
# pip install numpy pyzmq


if len(sys.argv) < 2 or len(sys.argv) >3:
	print "Usage: %s <ip address> <port number (defaults to 1337)>"%(sys.argv[0])
	sys.exit(1)

port_num = 1337
if len(sys.argv) == 3:
	port_num = int(sys.argv[2])

# First, try to connect to audio plugin:
ctx = zmq.Context()
socket = ctx.socket(zmq.PAIR)
socket.connect("tcp://%s:%d"%(sys.argv[1], port_num))

# Next, open up audio interface
BUFFLEN = 1024
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paFloat32, input=True, channels=1, rate=44100, frames_per_buffer=BUFFLEN)
failures = 0

# Now, capture audio, send statistics to ZMQ buddy
print "Capturing audio..."
while True:
	try:
		# Convert input audio stream to a float32 buffer
		audio_data = fromstring(stream.read(BUFFLEN), dtype=float32)

		# Take the standard deviation of the input audio data, amp it up by a factor of 6.
		# The 6 is completely arbitrary here.  It just seemed to work well.
		avg = 6*std(audio_data)

		# Send a binary representation of a floating point number across the socket
		socket.send(struct.pack("!f", avg))
	except IOError:
		print "ERROR: audio stream reading failed, retrying..."
		failures += 1
		if failures > 6:
			print "Max failures reached: quitting"
			break
	except KeyboardInterrupt:
		# This happens when you press CTRL-C
		break

print "Quitting gracefully..."