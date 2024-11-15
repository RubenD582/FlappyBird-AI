import pygame

class Ground(pygame.sprite.Sprite):
    SPEED = 2

    width, height = 0, 0
    x, y = 0, 0

    def __init__(self, x, HEIGHT):
        super().__init__()

        self.image = pygame.image.load("images/base.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.width, self.height = self.image.get_size()
        self.x, self.y = x, HEIGHT - self.height

        self.rect.topleft = (self.x, self.y)


    def update(self, x, game_over):
        if not game_over:
            self.x = x

        # Redraw the floor
        self.rect.topleft = (self.x, self.y)


    def get_position_x(self):
        return self.x
    
    def get_position_y(self):
        return self.y
    

    def get_width(self):
        return self.width
