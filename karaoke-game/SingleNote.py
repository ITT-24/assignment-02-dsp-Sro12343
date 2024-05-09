import pyglet
from pyglet import shapes

class SingleNote():
    def __init__(self, length, y_position, starting_x, note_size_y,y_scale, message,is_silent):
        self.y_position = y_position
        self.length = length
        self.note_size_y = note_size_y
        self.starting_x = starting_x
        self.x = self.starting_x
        self.normal_color = (100,100,100)
        self.hit_color = (100,255,100)
        self.was_played = False
        self.y_scale = y_scale
        self.message = message
        self.shape = None 
        self.is_silent= is_silent
         
        
    #def get_y_position(self):
    #    return self.y_position 

    #def getLength(self):
    #    return self.length
    
    def playNote(self):
        self.was_played = True
        return self.message   
    
    #def checkIfPlayed(self):
    #    return self.was_played
    
    def setIsHit(self, is_hit):
        if self.shape != None: 
            if is_hit:
                self.shape.color = self.hit_color
            else:
                self.shape.color = self.normal_color
       
    #def getIsHit(self):
    #   return self.is_hit
    
    #def checkCollision(self):
    #    pass        
            
    def draw(self):
        if self.shape == None: 
            self.shape = shapes.Rectangle(x=self.starting_x,y=self.y_position,width=self.length,height=self.note_size_y)
        else:
            self.shape.x = self.x
            self.shape.draw()