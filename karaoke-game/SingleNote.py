from pyglet import shapes

class SingleNote():
    def __init__(self, length, y, starting_x, note_size_y, message,is_silent):
        # Initialize instance variables
        self.y = y
        self.length = length
        self.note_size_y = note_size_y
        self.starting_x = starting_x
        self.x = self.starting_x
        self.normal_color = (75,75,75)
        self.hit_color = (200,200,200)
        self.was_played = False
        self.message = message
        self.shape = None 
        self.is_silent= is_silent
        
    def play_note(self):
        #marke the note as having being played
        self.was_played = True
        return self.message  
     
    def set_color(self, is_hit):
        #set color of the note wether it was hit or missed
        if self.shape != None: 
            if is_hit:
                self.shape.color = self.hit_color
            else:
                self.shape.color = self.normal_color
       
    def draw(self):
        if self.shape == None:
            # Create a new shape if it doesn't exist 
            self.shape = shapes.Rectangle(x=self.starting_x,y=self.y,width=self.length,height=self.note_size_y)
        else:
            # Update the existing shape's x-coordinate and draw it
            self.shape.x = self.x
            self.shape.draw()