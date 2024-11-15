import pygame

class MenuSprite(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height):
        super().__init__()

        self.image = pygame.image.load("images/message.png").convert_alpha()
        self.rect = self.image.get_rect()

        width, height = self.image.get_size()

        self.rect.topleft = (
            window_width // 2 - width/2, 
            window_height // 2 - height/2 - 50
        )

        self.visible = True


    def update(self, hide):
        self.visible = not hide


    def draw(self, surface):
        if self.visible:
            surface.blit(self.image, self.rect)