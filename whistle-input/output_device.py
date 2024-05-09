#The method for making the output came from https://pynput.readthedocs.io/en/latest/keyboard.html
from pynput.keyboard import Key, Controller
class output_device():
    def __init__(self):
        self.keyboard = Controller()
        pass
        
    def scroll(self,direction):
        if direction == "scroll_up":
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)        
            pass
        if direction == "scroll_down":
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)   
            pass
        