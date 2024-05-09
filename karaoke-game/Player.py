from pyglet import shapes
class Player():
    def __init__(self,starting_x,starting_y,size,step_size):
        
        #Initialize a Player object.
        self.x = starting_x
        self.y = starting_y
        self.step_size = step_size
        self.size_x = size
        self.size_y = size 
        self.shape = shapes.Rectangle(x=self.x,y=self.y,width=self.size_x,height=self.size_y,color=(225,225,225,225))
    
    def update_y(self,frequency):
        #Update the player's y
        if frequency != None:
            #set player y to sung frequency
            self.y =frequency * self.step_size
        else:
            #set player outside of screen
            self.y =  self.step_size *20
        self.shape.y = self.y

    def draw(self):
        self.shape.draw()