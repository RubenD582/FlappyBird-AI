import pygame
import random
from network import NeuralNetwork

class Player(pygame.sprite.Sprite):  
    def __init__(self, HEIGHT, neural_network = None):
        super().__init__() 

        color = f"images/AI/{random.randint(0, 3)}1.png"

        self.images = [
            pygame.image.load(color).convert_alpha(),
            pygame.image.load(color).convert_alpha(),
            pygame.image.load(color).convert_alpha()
        ]

        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        self.fitness = 0
        self.score = 0

        self.width, self.height = self.image.get_size()

        self.delay = 1  # Delay between frame updates (in milliseconds)
        self.last_update = pygame.time.get_ticks()

        self.x = 25
        # self.y = HEIGHT // 2 - 50
        self.y = random.randint(0, HEIGHT - 250)
        self.rect.topleft = (self.x, self.y)

        self.vx = 0
        self.vy = 0
        self.gravity = 0.5
        self.alive = True

        if neural_network is None:
            self.neural_network = NeuralNetwork(6, 15, 1)
        else:
            self.neural_network = neural_network

    def update(self):
        # Update position
        if self.alive:
            now = pygame.time.get_ticks()
            if now - self.last_update > self.delay:
                self.last_update = now
                self.index = (self.index + 1) % len(self.images)
                self.image = self.images[self.index]


            self.score += 0.1


            # Apply gravity
            self.vy += self.gravity

            self.x += self.vx
            self.y += self.vy

            # Rotate the player based on vertical velocity
            if self.vy > 0:
                self.image = pygame.transform.rotate(self.images[self.index], self.lerp(self.vy, 0, -7, 0, 20))  # Rotate clockwise
            elif self.vy < 0:
                self.image = pygame.transform.rotate(self.images[self.index], self.lerp(self.vy, 0, 20, 0, -20))  # Rotate counterclockwise

        # Update rectangle position
        self.rect.topleft = (self.x, self.y)


    def jump(self):
        self.vy = -7


    def get_vy(self):
        return self.vy


    def get_position_x(self):
        return self.x
    

    def get_position_y(self):
        return self.y
    

    def get_height(self):
        return self.height
    

    def get_width(self):
        return self.width
    

    def get_score(self):
        return self.score
    

    def set_y(self):
        self.y = random.randint(0, self.HEIGHT - 100)


    def get_network(self):
        return self.neural_network
    

    def lerp(self, value, start_min, start_max, end_min, end_max):
        # Calculate the percentage of the value between start_min and start_max
        percentage = (value - start_min) / (start_max - start_min)
        # Map the percentage to the range between end_min and end_max
        return end_min + percentage * (end_max - end_min)
