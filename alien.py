import pygame
import random


class Alien(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"image/alien_{type}.png"
        self.original_image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.original_image, (70, 50))  # Width=100, Height=75
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, direction):
        self.rect.x += direction


class MysteryShip(pygame.sprite.Sprite):
    def __init__(self, window_width, offset):
        super().__init__()
        self.original_image = pygame.image.load("image/mysteryship.png")
        self.offset = offset
        self.image = pygame.transform.scale(self.original_image, (70, 50))  # Width=100, Height=75
        self.window_width = window_width
        x = random.choice([self.offset/2, self.window_width + self.offset - self.image.get_width()])
        if x == self.offset/2:
            self.speed = 3
        else:
            self.speed = -3
        self.rect = self.image.get_rect(topleft=(x, 50))

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > self.window_width + self.offset/2:
            self.kill()
        elif self.rect.left < self.offset/2:
            self.kill()
