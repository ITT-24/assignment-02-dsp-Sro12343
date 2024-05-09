import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import pyglet
from pyglet.window import key
import mido

from directionCalculator import DirCalculator
from inputVisualizer import inputVisualizer
from output_device import output_device





# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 2048#600#1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
p = pyaudio.PyAudio()


#setup frequency calculator
input_calc = DirCalculator(RATE)

#setup output device
output = output_device()




# print info about audio devices
# let user select audio device
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

print('select audio device:')
input_device = int(input())

# open audio input stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=input_device)

       


#set pyglet window
WINDOW_SIZE_X = 768
WINDOW_SIZE_Y = 704
window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)
input_vis = inputVisualizer()

@window.event
def on_draw():
    window.clear()        
    # Read audio data from stream
    data = stream.read(CHUNK_SIZE)
    # Convert audio data to numpy array
    direction = input_calc.update(data)
    #print(direction)
    
    #this shows the input visualisation/simple gui demonstation
    input_vis.scroll(direction)
    input_vis.draw()
    
    #this makes the scroll into an output
    output.scroll(direction)    
    
    
def update(dt):
    input_calc.lowerTimer(dt)

pyglet.clock.schedule_interval(update, 1/15.0)            
pyglet.app.run()
        