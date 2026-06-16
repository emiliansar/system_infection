from classes.class_Battlefield import Battlefield

class Game:
    def __init__(self, screen):
        self.scr = screen
        self.width = self.scr.get_width()
        self.height = self.scr.get_height()

        self.battlefield = Battlefield(self.scr)
    
    def move(self):
        self.battlefield.move()

    def draw(self):
        self.scr.fill((0, 0, 0))
        self.battlefield.draw()