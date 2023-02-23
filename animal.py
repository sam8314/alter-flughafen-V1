import pygame
from settings import *
from support import * 
from timer import Timer

class Animal(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups, player):

        #general setup
        super().__init__(groups)
        self.collision_sprites = pygame.sprite.Group()
        self.sprite_type = 'animal'
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2
        self.name = name
        self.z = LAYERS['main']

        #graphic setup
        self.status = 'down_idle'
        self.image = pygame.Surface((21,16))
        self.rect = self.image.get_rect(midtop = pos)
        self.import_assets()
        self.image = self.animations[self.status][self.frame_index]

        #movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 180

        #collision 
        #self.hitbox = self.rect.copy()
        self.hitbox = self.rect.copy().inflate((-126,-70))

        #behaviour
        self.player = player
        self.impact = {
            'direction' : pygame.math.Vector2,
            'status' : 'down_idle'
        }
        self.timers = {
            'running away': Timer(1000, func = self.reset, activefunc = self.run_away)
        }

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if direction == 'horizontal':
                    if self.direction.x > 0: # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx

                if direction == 'vertical':
                    if self.direction.y > 0: # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery

    def move(self, dt):
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

    def import_assets(self): 
        self.animations = {'up': [],'down': [],'left': [],'right': [],
                        'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[]}

        for animation in self.animations.keys():
            full_path = '../graphics/animals/' + self.name +'/' + animation
            #full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self,dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def get_status(self):
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

    def behaviour(self, dt):
        if pygame.math.Vector2.distance_to(self.pos,self.player.pos) <=150 and self.player.speed > 40:
            self.impact['direction'] = self.player.direction
            self.impact['status'] = self.player.status        
            self.timers['running away'].activate()

    def run_away(self):
        self.direction = self.impact['direction']
        self.status = self.impact['status']
            
    def reset(self):
        self.direction.x = 0
        self.direction.y = 0
        self.status = 'right_idle'

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()

    def update(self, dt):
        self.get_status()
        self.behaviour(dt)
        self.move(dt)
        self.collision(self.direction)
        self.update_timers()
        self.animate(dt)
