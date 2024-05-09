import pyaudio
import numpy as np
from matplotlib import pyplot as plt
import pyglet
from pyglet.window import key
import mido

from GameLogic import GameLogic
from MenuLogic import MenuLogic
from freqencyCalculator import FreqCalculator

#set pyglet window
WINDOW_SIZE_X = 768
WINDOW_SIZE_Y = 704
window = pyglet.window.Window(WINDOW_SIZE_X, WINDOW_SIZE_Y)



# Set up audio stream
# reduce chunk size and sampling rate for lower latency
CHUNK_SIZE = 2048#600#1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1  # Mono audio
RATE = 44100  # Audio sampling rate (Hz)
p = pyaudio.PyAudio()


f_calc = FreqCalculator(RATE)
game_state = 0

# print info about audio devices
# let user select audio device
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

for i in range(0, numdevices):
    if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
        print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

print('select audio device:')
input_device = int(input())

OUTPUT_PORT = None
output_devices = mido.get_output_names()
if(len(output_devices)>0):
    for i in range(0,len(output_devices)):
        print("Output Device id ",i," - ", output_devices[i])
#    if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
#        print("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    print('select audio output device:')
    
    output_index= int(input())
    OUTPUT_PORT = OUTPUT_PORT = mido.open_output(output_devices[output_index])

# open audio input stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK_SIZE,
                input_device_index=input_device)


#Set up menu
#OUTPUT_PORT = mido.open_output('Microsoft GS Wavetable Synth 0')
menu_inst = MenuLogic(WINDOW_SIZE_X,WINDOW_SIZE_Y,OUTPUT_PORT)

GAME_SPEED = 300
game_inst = GameLogic(WINDOW_SIZE_X,WINDOW_SIZE_Y,OUTPUT_PORT,GAME_SPEED)


menu_inst.updateSong()

# continuously capture and plot audio singal
@window.event
def on_draw():
    window.clear()
    
    if game_state == 0:
        menu_inst.draw()
    elif game_state == 1:        
        game_inst.draw()

def update(dt):
    #updating seperatly from on_draw to have access to deltatime
    global game_state
    if game_state == 1:  
        # Read audio data from stream
        data = stream.read(CHUNK_SIZE)
        # Convert audio data to numpy array
        frequency = f_calc.update(data)
        #print(frequency)
        game_inst.update(frequency,dt)
        
        if game_inst.checkIfGameFinished():
            game_state = 0
        
    
@window.event
def on_key_press(symbol, modifiers):
    global game_state
    if game_state == 0:
        if symbol == pyglet.window.key.UP:
            #change Up selection in menu
            menu_inst.selectionUp()
            pass
        elif symbol == pyglet.window.key.DOWN:
            #change Down selection in menu
            menu_inst.selectionDown()
            pass
        elif symbol == pyglet.window.key.ENTER:
            #get current selected track
            #give it to game_inst start.
            song = menu_inst.startGame()
            game_inst.start(song)
            game_state = 1
            pass
        
pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.app.run()
   


    


#load midi files
    
#handle Input depending if game is started or Menu is started one or the other should get the interaction


 