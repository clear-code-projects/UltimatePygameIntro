import pygame

import constants
from Obstacle import Obstacle


class Fly(Obstacle):

    def __init__(self):
        fly_frame_1 = pygame.image.load(constants.FLY_1).convert_alpha()
        fly_frame_2 = pygame.image.load(constants.FLY_2).convert_alpha()
        frames = [fly_frame_1, fly_frame_2]
        super().__init__(frames, constants.SKY)
