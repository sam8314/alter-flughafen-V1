import pygame
from settings import *

class Animal(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups):

        #general setup
        super().__init__(groups)
        self.sprite_type = 'animal'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2

        #graphic setup
        self.image = pygame.Surface((64,64))
        self.rect = self.image.get_rect(topleft=(pos))
        # normalizing a vector 
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')