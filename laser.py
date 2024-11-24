import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, position, speed, window_height, color):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(center=position)
        self.speed = speed
        self.window_height = window_height

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.window_height + 15 or self.rect.y < 0:
            print("Laser killed")
            self.kill()
