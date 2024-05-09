from SingleNote import SingleNote

import pyglet
import threading
from mido import MidiFile
from Player import Player

class GameLogic():
    def __init__(self,window_size_x,window_size_y,output_port,speed):
        
        self.note_list = []
        self.playbackFinished = False 
        self.gameStarted = False
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        self.output_port = output_port
        self.song = None
        
        self.note_length_factor = speed
        self.y_scale = 20
        self.speed = speed
        self.player_starting_x = 100
        
        self.player = Player(self.player_starting_x, 100,40,self.y_scale)
        self.counter = 0
        
        self.Point_Lable = pyglet.text.Label(text="Points: ", x=window_size_x/2-200, y=600,color=(100,100,100,255))        
        self.Point_Counter = pyglet.text.Label(text="-", x=window_size_x/2, y=600,color=(100,100,100,255))

        pass
    
    def start(self,song):
        self.counter = 0
        self.spawnNotes(song)
        pass
    

    
    def spawnNotes(self,song):
        self.song = song
        def play():
            self.gameStarted = True
            for msg in MidiFile(self.song).play():
                is_silen = False
                if msg.velocity != 0:
                    is_silen = True
                    
                length = msg.time * self.speed
                y_position = (msg.note %12) * 600/12 -20 #*self.y_scale -800
                
                self.note_list.append(SingleNote(length,y_position,self.window_size_x,40,self.y_scale,msg,is_silen))
                      
                    
        self.song_thread = threading.Thread(target=play)
        self.song_thread.start()
    
    def checkIfGameFinished(self):
        
        
        if self.gameStarted ==True and not self.song_thread.is_alive() and len(self.note_list) == 0:
            print(str(self.gameStarted) + " " + str(self.song_thread.is_alive()) + " "+ str(len(self.note_list)))
            
            return True
        return False
    
    def checkCollision(self):
        #check along x achsys
        for n in self.note_list:
            #n.checkCollision(self.player.x, self.player.y)            
            if n.x  <= self.player_starting_x and n.x + n.length >= self.player_starting_x:
                #Check along y achsys
                if n.y_position <= self.player.y and self.player.y + n.note_size_y >= self.player.y:
                    #note is hit
                    n.setIsHit(True)
                    self.counter += 1
                    continue
            #note is not hit    
            n.setIsHit(False)
     
        
        
    def update(self,frequency,dt):
        self.player.update_hight(frequency)
        for n in self.note_list:
            
            n.x -=self.speed *dt
            if n.x<=0 and n.was_played == False:
                msg = n.playNote()
                self.output_port.send(msg)
            #n.update()     
            if n.x<=-n.length:
                if n.shape != None:
                    n.shape.delete()
                self.note_list.remove(n)
        self.checkCollision()
        self.Point_Counter.text = str(self.counter)

    def draw(self):
        for n in self.note_list:
            if n.is_silent == False:
                n.draw()
                
        self.player.draw()
        self.Point_Counter.draw()
        self.Point_Lable.draw()
        pass
    
    
    