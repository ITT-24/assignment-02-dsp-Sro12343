from pyglet import shapes
class Player():
    def __init__(self,starting_x,starting_y,size,y_scale):
        self.x = starting_x
        self.y = starting_y
        self.y_scale = y_scale
        self.width = size
        self.height = size 
        self.shape = shapes.Rectangle(x=self.x,y=self.y,width=self.width,height=self.height,color=(225,225,225,225))
        pass
    
    def update_hight(self,hight):
        if hight != None:
            self.y =hight * 600/12 - (self.width/2)
            self.shape.y = self.y
        else:
            self.y = 1000
        pass
    def draw(self):
        self.shape.draw()