import pygame
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip
import random


class Game:
    def __init__(self, window_width, window_height, offset):
        self.offset = offset
        self.window_width = window_width
        self.window_height = window_height
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.window_width, self.window_height, self.offset))
        self.aliens_group = pygame.sprite.Group()
        self.alien_alive = 0
        self.create_aliens()
        self.obstacles = self.create_obstacles()
        self.alien_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.Group()
        self.lives = 3
        self.run = True
        self.score = 0
        self.highscore = 0
        self.load_highscore()
        pygame.mixer.music.load("sound/music.ogg")
        pygame.mixer.music.play(-1)
        self.explosion_sound = pygame.mixer.Sound("sound/explosion.ogg")

    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.window_width + self.offset - (4 * obstacle_width)) / 5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.window_height - 150)
            obstacles.append(obstacle)
        return obstacles

    def create_aliens(self):
        for row in range(3):
            for column in range(10):
                x = 90 + column * 60
                y = 100 + row * 60

                if row == 1:
                    alien_type = 1
                elif row == 2:
                    alien_type = 2
                else:
                    alien_type = 5

                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_group.add(alien)

    def move_aliens(self):
        self.aliens_group.update(self.alien_direction)
        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.window_width + self.offset/2:
                self.alien_direction = -2
                self.alien_move_down(1)
            elif alien.rect.left <= self.offset/2:
                self.alien_direction = 2
                self.alien_move_down(1)

    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance

    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.window_height, (0, 255, 0))
            self.alien_lasers_group.add(laser_sprite)

    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.window_width, self.offset))

    def check_for_collisions(self):
        self.alien_alive = len(self.aliens_group)
        # Spaceship
        if self.spaceship_group.sprite.laser_group:
            for laser_sprite in self.spaceship_group.sprite.laser_group:
                alien_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if alien_hit:
                    self.explosion_sound.play()
                    for alien in alien_hit:
                        self.score += alien.type * 100
                        self.alien_alive -= 1
                        self.check_for_highscore()
                        laser_sprite.kill()
                        if self.alien_alive == 0:
                            self.run = False

                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.score += 1000
                    self.explosion_sound.play()
                    self.check_for_highscore()
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.block_group, True):
                        laser_sprite.kill()

        # Alien  Lasers
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.block_group, True):
                        laser_sprite.kill()

        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.block_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()

    def game_over(self):
        self.run = False

    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.obstacles = self.create_obstacles()
        self.score = 0

    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))

    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0

    def remove(self):
        for alien in self.aliens_group:
            alien.kill()
        for laser in self.alien_lasers_group:
            laser.kill()
        for laser in self.spaceship_group.sprite.laser_group:
            laser.kill()
        for mystery_ship in self.mystery_ship_group:
            mystery_ship.kill()
