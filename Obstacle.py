from random import randint

import pygame

import constants


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, frames, y_position):
        super().__init__()
        self.animation_index = 0
        self.y_pos = y_position
        self.frames = frames
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomleft=(constants.SCREEN_WIDTH + randint(0, 200), self.y_pos))
        self.gravity = 0

    def player_input(self):
        pressed, _, _ = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        if pressed and self.rect.bottom >= self.y_pos and self.rect.collidepoint(pos):
            self.gravity = constants.WEAK_JUMP

    def apply_gravity(self):
        if self.gravity < 100:
            self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= self.y_pos:
            self.rect.bottom = self.y_pos

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.rect.x -= constants.OBSTACLE_MOVEMENT_SPEED
        if self.rect.x <= -100:
            self.kill()
