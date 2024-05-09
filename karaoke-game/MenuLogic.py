import os.path
import pyglet
import mido
from mido import MidiFile

import time
from MenuSongPlayer import songPlayer

class MenuLogic:
    def __init__(self,window_size_x,window_size_y,outputPort):
        self.song_index = 0
        self.song_list = []
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y

        self.outputPort = outputPort
        self.current_dir = os.path.dirname(__file__)
        self.music_folder = os.path.join(self.current_dir,'music')

        self.fillList(self.music_folder)
        self.max_song_index = len(self.song_list) -1
        
        self.song_previous = pyglet.text.Label(text="-", x=window_size_x/2, y=150,color=(100,100,100,255), anchor_x='center',anchor_y='center')
        self.song_selected = pyglet.text.Label(text="-", x=window_size_x/2, y=100,color=(255,255,255,255), anchor_x='center',anchor_y='center')
        self.song_next = pyglet.text.Label(text="-", x=window_size_x/2, y=50,color=(100,100,100,255), anchor_x='center',anchor_y='center')
        
        self.songPlayer = songPlayer(self.music_folder,self.song_list[0],self.outputPort)
        self.updateText()
        
        self.lastScore = 0
        self.last_score_counter = pyglet.text.Label(text="-", x=window_size_x/2, y=500,color=(100,100,100,255), anchor_x='center',anchor_y='center')
    
    
    def fillList(self, folder):
        #Fill list of songs with all Songs in music folder
        files_in_folder = os.listdir(folder)
        for file in  files_in_folder:
            if file.endswith(".mid"):
                self.song_list.append(file)
    
    def selectionUp(self):
        if self.song_index -1 >=0:
            self.song_index -=1
            self.updateText() 
            self.updateSong()
            
    def selectionDown(self):
        if self.song_index +1 <= self.max_song_index:
            self.song_index +=1
            self.updateText() 
            self.updateSong()
    
    def updateText(self):
        
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
        
    def updateSong(self):
        #Change Playing Song
        self.songPlayer.stopPlay()
        self.songPlayer = songPlayer(self.music_folder,self.song_list[self.song_index],self.outputPort)
        self.songPlayer.playSong()
        
    def updateScore(self,score):
        self.lastScore = score
        self.last_score_counter.text = "Last Score: " + str(self.lastScore)
    
    def startGame(self):
        #Return current Song
        self.songPlayer.stopPlay()
        result = os.path.join(self.music_folder,self.song_list[self.song_index])
        print(result)
        return result
    
    def draw(self):
        self.song_previous.draw()
        self.song_selected.draw()
        self.song_next.draw()
        if self.lastScore !=0:
            self.last_score_counter.draw()




   