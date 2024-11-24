# CREDIT : Programming With Nick - YouTube

# CREDIT Images :
# spaceship : Flaticon
# mysteryship : PNGkey.com
# alien_1 : PikPng.com
# alien_2 : PNGall.com
# alien_5: PNGall.com


import pygame
import sys
import random
from game import Game

GREY = (29, 29, 27)
GREEN = (0, 255, 0)

pygame.init()

font = pygame.font.Font("font/monogram.ttf", 40)
over_font = pygame.font.Font("font/monogram.ttf", 150)
level_text = font.render("LEVEL 01", False, GREEN)
game_over_text = over_font.render("GAME OVER", False, GREEN)
score_text = font.render("SCORE", False, GREEN)
highscore_text = font.render("HIGH SCORE", False, GREEN)
restart_text = font.render("Press space to restart", False, GREEN)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
OFFSET = 50

screen = pygame.display.set_mode((WINDOW_WIDTH + OFFSET, WINDOW_HEIGHT + 2 * OFFSET))
pygame.display.set_caption("Space Invaders")

clock = pygame.time.Clock()
game = Game(WINDOW_WIDTH, WINDOW_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 500)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()
        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and game.run == False:
            game.reset()

    # Draw object
    screen.fill(GREY)
    pygame.draw.rect(screen, GREEN, (10, 10, 830, 680), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, GREEN, (25, 620), (825, 620), 3)

    if game.run:
        screen.blit(level_text, (600, 640, 50, 50))
    else:
        screen.blit(game_over_text, (175, 200, 50, 50))
        screen.blit(restart_text, (460, 635, 50, 50))
        game.remove()

    x = 70
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 630))
        x += 70

    screen.blit(score_text, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score = font.render(formatted_score, False, GREEN)
    screen.blit(score, (50, 40, 50, 50))
    screen.blit(highscore_text, (650, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore = font.render(formatted_highscore, False, GREEN)
    screen.blit(highscore, (725, 40, 50, 50))

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.laser_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.block_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    # Update object
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    pygame.display.update()
    clock.tick(60)

# CREDIT : Programming With Nick - YouTube
