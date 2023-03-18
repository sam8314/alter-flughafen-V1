import pygame
from settings import *
from support import * 
from timer import Timer

class Animal(pygame.sprite.Sprite):
    def __init__(self, name, pos, groups, player, animal_collision_sprites):

        #general setup
        super().__init__(groups)
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
        self.hitbox = self.rect.copy().inflate((0,20))
        self.animal_collision_sprites = animal_collision_sprites

        #behaviour
        self.player = player
        self.impact = {
            'direction' : pygame.math.Vector2,
            'status' : 'down_idle'
        }
        self.timers = {
            'running away': Timer(1000, func = self.reset, activefunc = self.run_away)
        }
        self.soft_contact = False

    def collision(self, direction):
        for sprite in self.animal_collision_sprites.sprites():
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

    def opposite_status(self, status):
        if status == 'up':
            return 'down'
        elif status == 'down':
            return 'up'
        elif status == 'left':
            return 'right'
        elif status == 'right':
            return 'left'
        elif status == 'right_idle':
            return 'left_idle'
        elif status == 'left_idle':
            return 'right_idle'

    def getting_closer(self, pos, player_pos, player_dir):
        if (pos.x > player_pos.x and pos.y > player_pos.y and player_dir == [0.7071707,0.7071707]):
            return True
        elif (pos.x > player_pos.x and pos.y == player_pos.y and player_dir == [1,0]):
            return True
        elif (pos.x == player_pos.x and pos.y > player_pos.y and player_dir == [0,1]):
            return True
        elif (pos.x == player_pos.x and pos.y < player_pos.y and player_dir == [0,-1]):
            return True
        elif (pos.x < player_pos.x and pos.y < player_pos.y and player_dir == [-0.7071707,-0.7071707]):
            return True
        elif (pos.x < player_pos.x and pos.y == player_pos.y and player_dir == [-1,0]):
            return True
        elif (pos.x > player_pos.x and pos.y > player_pos.y and player_dir == [0,1]):
            return True
        elif (pos.x > player_pos.x and pos.y > player_pos.y and player_dir == [1,0]):
            return True
        elif (pos.x < player_pos.x and pos.y < player_pos.y and player_dir == [0,-1]):
            return True
        elif (pos.x < player_pos.x and pos.y < player_pos.y and player_dir == [-1,0]):
            return True
        else:
            return False

    def behaviour(self):
        if pygame.math.Vector2.distance_to(self.pos,self.player.pos) <=150 and self.player.speed > 40:
            if self.getting_closer(self.pos, self.player.pos, self.player.direction):#player goes closer towards the animal
                self.impact['direction'] = self.player.direction
                self.impact['status'] = self.player.status        
                self.timers['running away'].activate()
            else: #player takes other direction
                if not self.player.direction.length() == 0: #îf plaer is moving
                    self.impact['direction'] = pygame.math.Vector2.reflect(self.player.direction,self.player.direction)
                    self.impact['status'] = self.opposite_status(self.player.status)        
                    self.timers['running away'].activate()
        
        if pygame.math.Vector2.distance_to(self.pos, self.player.pos) < 60 and self.player.speed <= 50:
            self.soft_contact = True 
        else:
            self.soft_contact = False

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
        self.behaviour()
        self.move(dt)
        self.collision(self.direction)
        self.update_timers()
        self.animate(dt)
