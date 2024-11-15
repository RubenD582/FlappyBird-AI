import pygame
import random

class Pipe(pygame.sprite.Sprite):
    SPEED = 2
    GAP = 100
    
    width, height = 0, 0
    x, y = 0, 0

    def __init__(self, x, y, top = False):
        super().__init__()

        self.image = pygame.image.load("images/pipe.png").convert_alpha()
        if top:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()

        self.width, self.height = self.image.get_size()
        self.x = x
        self.y = -self.height + y
        
        self.rect.topleft = (self.x, self.y)


    def update(self, x):
        self.x = x

        # Redraw the floor
        self.rect.topleft = (self.x, self.y)

    
    def set_y(self, y):
        self.y = -self.height + y


    def set_x(self, x):
        self.x = x


    def get_position_x(self):
        return self.x
    
    
    def get_position_y(self):
        return self.y
    
    
    def get_height(self):
        return self.height
    

    def get_width(self):
        return self.width