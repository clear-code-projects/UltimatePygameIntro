from random import choice
from sys import exit

import pygame

import constants
from Fly import Fly
from GameMenuScreen import GameMenuScreen
from Player import Player
from Snail import Snail

sky_surf = pygame.image.load(constants.SKY_BACKGROUND)
ground_surf = pygame.image.load(constants.GROUND_BACKGROUND)


def main():
    screen = init_screen()
    clock = pygame.time.Clock()
    font = pygame.font.Font(constants.FONT, constants.FONT_SIZE)
    game_menu_screen = GameMenuScreen(screen, font)

    music = pygame.mixer.Sound(constants.AUDIO_BACKGROUND)
    music.set_volume(0.01)
    music.play(loops=-1)

    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 1500)

    player_group = pygame.sprite.GroupSingle()
    player = Player()
    player_group.add(player)

    obstacle_group = pygame.sprite.Group()

    game_active = False
    start_time = 0
    end_time = 0
    current_score = 0

    while True:
        for event in pygame.event.get():
            do_quit(event)
            if game_active:
                if event.type == pygame.KEYDOWN:
                    player.do_jump()
                if event.type == obstacle_timer:
                    obstacle_group.add(choice([Snail(), Snail(), Snail(), Fly()]))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and (
                    (pygame.time.get_ticks() - end_time > 500) or end_time == 0):
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

        if game_active:
            set_background(screen)
            current_score = display_score(screen, start_time, font)

            player_group.draw(screen)
            player_group.update()

            obstacle_group.draw(screen)
            obstacle_group.update()

            if pygame.sprite.spritecollide(player_group.sprite, obstacle_group, False):
                game_active = False
                end_time = pygame.time.get_ticks()
                obstacle_group.empty()

        else:
            game_menu_screen.show(current_score)

        pygame.display.update()
        clock.tick(60)


def display_score(screen, start_time, font):
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def set_background(screen):
    screen.blit(sky_surf, (0, 0))
    screen.blit(ground_surf, (0, constants.FLOOR))


def init_screen():
    pygame.init()
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption(constants.GAME_NAME)
    return screen


def do_quit(event):
    if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
        pygame.quit()
        exit()


if __name__ == "__main__":
    main()
