#The method for making the output came from https://pynput.readthedocs.io/en/latest/keyboard.html
from pynput.keyboard import Key, Controller
class output_device():
    def __init__(self):
        self.keyboard = Controller()
        pass
        
    def scrole(self,direction):
        if direction == "scrole_up":
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)        
            pass
        if direction == "scrole_down":
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)   
            pass
        