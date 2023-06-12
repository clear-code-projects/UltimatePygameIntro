import pygame

import constants


class GameMenuScreen:

    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.game_logo = pygame.image.load(constants.PLAYER_STAND).convert_alpha()
        self.game_logo = pygame.transform.scale2x(self.game_logo)
        self.game_logo_rect = self.game_logo.get_rect(center=(constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2))

        self.game_name = self.font.render(constants.GAME_NAME, False, constants.HOME_SCREEN_TEXT_COLOR)
        self.game_name_rect = self.game_name.get_rect(center=(constants.SCREEN_WIDTH / 2, 80))

        self.game_msg = self.font.render("Press space to run", False, constants.HOME_SCREEN_TEXT_COLOR)
        self.game_msg_rect = self.game_msg.get_rect(center=(constants.SCREEN_WIDTH / 2, 340))

        self.game_continue_msg = font.render("Press space to run again", False, constants.HOME_SCREEN_TEXT_COLOR)
        self.game_continue_msg_rect = self.game_continue_msg.get_rect(center=(constants.SCREEN_WIDTH / 2, 340))

    def show(self, score):
        self.screen.fill(constants.HOME_SCREEN_COLOR)
        self.screen.blit(self.game_logo, self.game_logo_rect)
        if score:
            score_surf = self.font.render(f'Your Score: {score}', False, constants.HOME_SCREEN_TEXT_COLOR)
            score_surf_rect = score_surf.get_rect(center=(constants.SCREEN_WIDTH / 2, 80))
            self.screen.blit(score_surf, score_surf_rect)
            self.screen.blit(self.game_continue_msg, self.game_continue_msg_rect)
        else:
            self.screen.blit(self.game_name, self.game_name_rect)
            self.screen.blit(self.game_msg, self.game_msg_rect)
