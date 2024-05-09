import os.path
import pyglet
import mido
from mido import MidiFile

import time
from MenuSongPlayer import songPlayer

class MenuLogic:
    def __init__(self,window_size_x,window_size_y,output_port):
        # Initialize instance variables 
        self.song_index = 0
        self.song_list = []
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        self.output_port = output_port
        self.current_dir = os.path.dirname(__file__)
        self.music_folder = os.path.join(self.current_dir,'music')
        self.fill_list(self.music_folder)
        self.max_song_index = len(self.song_list) -1
        self.song_previous = pyglet.text.Label(text="-", x=window_size_x/2, y=150,color=(100,100,100,255), anchor_x='center',anchor_y='center')
        self.song_selected = pyglet.text.Label(text="-", x=window_size_x/2, y=100,color=(255,255,255,255), anchor_x='center',anchor_y='center')
        self.song_next = pyglet.text.Label(text="-", x=window_size_x/2, y=50,color=(100,100,100,255), anchor_x='center',anchor_y='center')
        
        self.song_player = songPlayer(self.music_folder,self.song_list[0],self.output_port)
        self.update_text()
        
        self.last_score = 0
        self.last_score_counter = pyglet.text.Label(text="-", x=window_size_x/2, y=500,color=(100,100,100,255), anchor_x='center',anchor_y='center')
    
    
    def fill_list(self, folder):
        #Fill list of songs with all Songs in music folder
        files_in_folder = os.listdir(folder)
        for file in  files_in_folder:
            if file.endswith(".mid"):
                self.song_list.append(file)
    
    def selection_up(self):
        #Scroll up in list if it is possible
        if self.song_index -1 >=0:
            self.song_index -=1
            self.update_text() 
            self.update_song()
            
    def selection_down(self):
        #Scroll down in list if it is possible
        if self.song_index +1 <= self.max_song_index:
            self.song_index +=1
            self.update_text() 
            self.update_song()
    
    def update_text(self):
        
        #Update Song Title Display for Previous Song
        if self.song_index -1 >=0:
            self.song_previous.text = self.song_list[self.song_index-1]
        else:
           self.song_previous.text = "" 
        
        #Update Song Title Display for Selected Song
        self.song_selected.text = self.song_list[self.song_index]
        
        
        #Update Song Title Display for Next Song
        if self.song_index +1 <=self.max_song_index:
            self.song_next.text = self.song_list[self.song_index+1]
        else:
           self.song_next.text = ""
        
    def update_song(self):
        #Change Playing Song
        self.song_player.stop_play()
        self.song_player = songPlayer(self.music_folder,self.song_list[self.song_index],self.output_port)
        self.song_player.play_song()
        
    def stop_song(self):
        #stop song
        self.song_player.stop_play()
        
    def update_score(self,score):
        #change score to the transmitted score
        self.last_score = score
        self.last_score_counter.text = "Last Score: " + str(self.last_score)
    
    def start_game(self):
        #Return current Song
        self.song_player.stop_play()
        result = os.path.join(self.music_folder,self.song_list[self.song_index])
        print(result)
        return result
    
    def draw(self):
        #Display the Song title texts
        self.song_previous.draw()
        self.song_selected.draw()
        self.song_next.draw()
        
        #if a game was played show its scored
        if self.last_score !=0:
            self.last_score_counter.draw()   