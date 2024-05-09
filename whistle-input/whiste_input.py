import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import pyglet
from pyglet.window import key
import mido

from directionCalculator import FreqCalculator
from inputVisualizer import inputVisualizer
from output_device import output_device

#set pyglet window
WINDOW_SIZE_X = 768
WINDOW_SIZE_Y = 704



# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 2048#600#1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
p = pyaudio.PyAudio()


f_calc = FreqCalculator(RATE)
output = output_device()
window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)
input_vis = inputVisualizer()

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


    
#while True:
#    # Read audio data from stream
#    data = stream.read(CHUNK_SIZE)
#    # Convert audio data to numpy array
#    direction = f_calc.update(data)
#    
#    input_vis.update(direction)
#    output.update(direction)
       

@window.event
def on_draw():
    window.clear()        
    # Read audio data from stream
    data = stream.read(CHUNK_SIZE)
    # Convert audio data to numpy array
    direction = f_calc.update(data)
    #print(direction)
    
    input_vis.scrole(direction)
    input_vis.draw()
    
    output.scrole(direction)    
    
    
def update(dt):
    f_calc.lowerTimer(dt)

pyglet.clock.schedule_interval(update, 1/15.0)            
pyglet.app.run()
        


   

#!!!! Migrate Draw event to inputVisualizer and use while true instead.