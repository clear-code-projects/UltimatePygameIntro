import pygame

import constants
from Obstacle import Obstacle


class Snail(Obstacle):

    def __init__(self):
        snail_frame_1 = pygame.image.load(constants.SNAIL_1).convert_alpha()
        snail_frame_2 = pygame.image.load(constants.SNAIL_2).convert_alpha()
        frames = [snail_frame_1, snail_frame_2]
        super().__init__(frames, constants.FLOOR)
