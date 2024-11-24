import pygame
from laser import Laser


class Spaceship(pygame.sprite.Sprite):
    def __init__(self, window_width, window_height, offset):
        super().__init__()
        self.offset = offset
        self.window_width = window_width
        self.window_height = window_height
        self.original_image = pygame.image.load("image/spaceship.png")
        self.image = pygame.transform.scale(self.original_image, (70, 50))  # Width=100, Height=75
        self.rect = self.image.get_rect(midbottom=((self.window_width + self.offset) / 2, self.window_height))
        self.speed = 6
        self.laser_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 300
        self.laser_sound = pygame.mixer.Sound("sound/laser.ogg")

    def get_user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.window_height, (255, 0, 0))
            self.laser_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    def constrain_movement(self):
        if self.rect.right > self.window_width:
            self.rect.right = self.window_width
        if self.rect.left < self.offset:
            self.rect.left = self.offset

    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True

    def update(self):
        self.get_user_input()
        self.constrain_movement()
        self.laser_group.update()
        self.recharge_laser()

    def reset(self):
        self.rect = self.image.get_rect(midbottom=((self.window_width + self.offset) / 2, self.window_height))
        self.laser_group.empty()

