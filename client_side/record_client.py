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

# Set to 0 for default input.  2 == soundflower right now.  until you somehow screw it up
dev_idx = 0
dev_info = pa.get_device_info_by_index(dev_idx)
print "Opening device %s (index %d)"%(dev_info['name'], dev_idx)


stream = pa.open(format=pyaudio.paFloat32, input_device_index=dev_idx, input=True, channels=1, rate=44100, frames_per_buffer=BUFFLEN)
failures = 0

# Now, capture audio, send statistics to ZMQ buddy
print "Capturing audio..."
last_val = 0
while True:
	try:
		# Convert input audio stream to a float32 buffer
		audio_data = fromstring(stream.read(BUFFLEN), dtype=float32)

		# Take the standard deviation of the input audio data, amp it up by a factor of 10.
		# The 10 is completely arbitrary here.  It just seemed to work well.
		input_val = 2.0*std(audio_data)
		output_val = input_val + 0.5*last_val
		last_val = input_val

		# Send a binary representation of a floating point number across the socket
		socket.send(struct.pack("!f", output_val))
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
