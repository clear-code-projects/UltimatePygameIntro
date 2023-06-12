import pygame

import constants


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.player_jump = pygame.image.load(constants.PLAYER_JUMP).convert_alpha()
        player_walk_1 = pygame.image.load(constants.PLAYER_WALK_1).convert_alpha()
        player_walk_2 = pygame.image.load(constants.PLAYER_WALK_2).convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(100, 300))
        self.gravity = 0;
        self.jump_remaining = constants.TOTAL_JUMPS
        self.jump_sound = pygame.mixer.Sound(constants.AUDIO_JUMP)
        self.jump_sound.set_volume(0.01)

    def do_jump(self):
        if self.jump_remaining > 0:
            if self.rect.bottom >= constants.FLOOR:
                self.gravity = constants.STRONG_JUMP
            else:
                self.gravity = constants.WEAK_JUMP
            self.jump_remaining -= 1
            self.jump_sound.play()

    def apply_gravity(self):
        if self.gravity < 100:
            self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= constants.FLOOR:
            self.rect.bottom = constants.FLOOR
            self.jump_remaining = constants.TOTAL_JUMPS

    def animation_state(self):
        if self.rect.bottom < constants.FLOOR:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.apply_gravity()
        self.animation_state()
