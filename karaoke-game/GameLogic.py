from SingleNote import SingleNote
import pyglet
from pyglet import shapes
import threading
from mido import MidiFile
from Player import Player
import os.path

class GameLogic():
    def __init__(self,window_size_x,window_size_y,output_port,speed): 
        # Initialize instance variables   
        self.note_list = []
        self.playback_finished = False 
        self.game_started = False
        self.force_stop_song = False
        self.window_size_x = window_size_x
        self.window_size_y = window_size_y
        self.output_port = output_port
        self.song = None
        self.speed = speed
        self.player_starting_x = 100
        self.player_starting_y = 100
        self.player_size= 40
        self.note_size_y = 40
        self.step_size = (window_size_y-100)/12
        self.player = Player(self.player_starting_x, self.player_starting_y,self.player_size,self.step_size)
        self.counter = 0
        #self.point_lable = pyglet.text.Label(text="Points: ", x=window_size_x/2-200, y=600,color=(50,50,50,255))        
        self.point_counter = pyglet.text.Label(text="-", x=10, y=650,color=(50,50,50,255))
        self.music_offset = 40 
       
        self.current_dir = os.path.dirname(__file__)
        self.title_image_p = os.path.join(self.current_dir,'images','background.jpeg')
        self.title_image = pyglet.image.load(self.title_image_p)
        self.background_image = pyglet.sprite.Sprite(img=self.title_image)

        self.lines = []
        self.fill_lines()
    
    def fill_lines(self):
        for i in range(12):
            self.lines.append(shapes.Rectangle(x=0,y=self.step_size*i+(self.note_size_y/2),width=900,height=2,color=(50,50,50,155))) 
    
    def start(self,song):
        #Starts the game with the given song.
        self.counter = 0
        self.spawn_notes(song)
        pass
        
    def spawn_notes(self,song):
        print('in spawn_notes')
        #Spawns notes for the given song.
        self.song = song
        def play():
            print('in play()')
            #Plays the MIDI file and spawns notes accordingly.
            self.game_started = True
            for msg in MidiFile(self.song).play():
                print(msg)
                #check if force stop song.
                if self.force_stop_song == True:
                    break
                #Skip control_change and program_change midi_mesages
                if msg.type != "control_change" and msg.type != "program_change":
                    
                    #if midi note is of type note_off or has a velocity of zero it can not be interacted with and is invisable
                    is_silent = False 
                    try:
                        if msg.type == "note_off" or msg.velocity == 0:
                            is_silent = True
                    except:
                        continue
                    #set note length
                    length = msg.time * self.speed
                    #set note y position according to pitch but not octave 
                    y_position = (msg.note %12) * self.step_size #-20
                    #add note
                    self.note_list.append(SingleNote(length,y_position,self.window_size_x,self.note_size_y,msg,is_silent))                   
            print('end play()')
        #spawn the notes in a thread, so it dose not stop the rest of the program
        #play()
        self.song_thread = threading.Thread(target=play, daemon=True)
        print('before start thread')
        self.song_thread.start()
        print('after start thread')
        #self.song_thread.join()
        #print('after join thread')

    def check_if_game_finished(self):    
        #Checks if the game has finished.    
        if self.game_started ==True and not self.song_thread.is_alive() and len(self.note_list) == 0:
            print(str(self.game_started) + " " + str(self.song_thread.is_alive()) + " "+ str(len(self.note_list)))
            return True
        return False

    def update(self,frequency,dt):
        #update y position along recognized frequency.
        self.player.update_y(frequency)
        
        #for eacj mpte
        for n in self.note_list:
            #move note to left
            n.x -=self.speed *dt
            
            #Play note if it has reached player and was not already played.
            #The offset means the music plays a bit befor the player needs to hit the notes, so the player knows what to sing.
            if n.x<=self.player.x +self.player.size_x + self.music_offset and n.was_played == False:
                msg = n.play_note()
                self.output_port.send(msg) 
                
            #check if note should despawn
            if n.x<=-n.length:
                if n.shape != None:
                    n.shape.delete()
                self.note_list.remove(n)
        #check collision betwen player and notes
        self.check_collision()
        #update point counter
        self.point_counter.text = "Points: "+str(self.counter)

    
    def check_collision(self):        
        for n in self.note_list:
        #for each note
            if n.is_silent == False:
            #only check further if  note is not silent    
                if n.x  <= self.player_starting_x and \
                n.x + n.length >= self.player_starting_x:
                #Check if note reached same x achsys as player
                    if self.player.y + self.player.size_y >= n.y and\
                    n.y + n.note_size_y >= self.player.y:
                    #check if note and player intersect in height.
                        #note is hit
                        n.set_color(True)
                        #increase point counter
                        self.counter += 1
                        #skip to next note
                        continue
                #note is not hit    
                n.set_color(False)
             

    def draw(self):
        
        #draw background image
        self.background_image.draw()
        
        for l in self.lines:
            l.draw()
        
        #draw visible notes
        for n in self.note_list:
            if n.is_silent == False:
                n.draw()   
        #draw player                
        self.player.draw()
        #draw point counter
        self.point_counter.draw()
