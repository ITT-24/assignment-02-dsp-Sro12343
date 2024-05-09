import mido
from mido import MidiFile
import os 




song_name = 'Tetris - Tetris Main Theme.mid'#'Beethoven-Moonlight-Sonata.mid'#'Sabaton — Wehrmacht [MIDIfind.com].mid'
current_dir = os.path.dirname(__file__)
music_p = os.path.join(current_dir,song_name)


output_port = mido.open_output('Microsoft GS Wavetable Synth 0')
msg = music_p

#for msg in MidiFile(music_p)[0]

#print(MidiFile(music_p).)
#output_port.send(msg)

print(mido.get_output_names())
for msg in MidiFile(music_p).play():
    print(msg)
    output_port.send(msg)
