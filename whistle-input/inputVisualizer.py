import pyglet
from pyglet import shapes

import numpy as np
class inputVisualizer():
    def __init__(self):
        # Initialize instance variables 
        self.box_list = []
        self.boxes_numb = 20
        self.box_index = 10
        self.normal_color = (100,100,100)
        self.highlight_color = (100,255,100)
        self.fillList()
        self.box_list[self.box_index].color = self.highlight_color
        pass
        
    def fillList(self):
    #fill the list with all the boxes
        for i in range(self.boxes_numb):
            self.box_list.append(shapes.Rectangle(x=100,y=35* i,width=600,height=30,color=(100,100,100,100)))

    def scroll_up(self):
        #check if can scroll up
        if self.box_index +1 < self.boxes_numb -1:
            #dehighlight old selection
            self.box_list[self.box_index].color = self.normal_color
            #move selection
            self.box_index += 1
            #highlight new selection
            self.box_list[self.box_index].color = self.highlight_color
    
    def scroll_down(self):
        #check if can scroll down
        if self.box_index -1 >= 0:
            #dehighlight old selection
            self.box_list[self.box_index].color = self.normal_color
            #move selection
            self.box_index -= 1
            #highlight new selection
            self.box_list[self.box_index ].color = self.highlight_color
            


    def scroll(self,direction):
        if direction == "scroll_up":
        #scroll up
            self.scroll_up()
        elif direction == "scroll_down":
        #scroll down
            self.scroll_down()
        
    
    def draw(self):
        #draw the boxes.
        for i in range(len(self.box_list)):
            self.box_list[i].draw()

    
   