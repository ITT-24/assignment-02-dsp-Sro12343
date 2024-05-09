import pyglet
from pyglet import shapes

import numpy as np
class inputVisualizer():
    def __init__(self):
        self.box_list = []
        self.boxes_numb = 20
        self.box_index = 10
        self.normal_color = (100,100,100)
        self.highlight_color = (100,255,100)
        self.fillList()
        self.box_list[self.box_index].color = self.highlight_color
        pass
        
    def fillList(self):
        for i in range(self.boxes_numb):
            self.box_list.append(shapes.Rectangle(x=100,y=35* i,width=600,height=30,color=(100,100,100,100)))

    def scrole_up(self):
        #check if can scrole up
        if self.box_index +1 < self.boxes_numb -1:
            #dehighlight old selection
            self.box_list[self.box_index].color = self.normal_color
            #move selection
            self.box_index += 1
            #highlight new selection
            self.box_list[self.box_index].color = self.highlight_color
    
    def scrole_down(self):
        #check if can scrole down
        if self.box_index -1 >= 0:
            #dehighlight old selection
            self.box_list[self.box_index].color = self.normal_color
            #move selection
            self.box_index -= 1
            #highlight new selection
            self.box_list[self.box_index ].color = self.highlight_color
            


    def scrole(self,direction):
        #print(self.box_index)
        if direction == "scrole_up":
            self.scrole_up()
            
            pass
        elif direction == "scrole_down":
            self.scrole_down()
            
            pass
        pass
        
    
    def draw(self):
        for i in range(len(self.box_list)):
            self.box_list[i].draw()

    
   