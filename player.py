import pygame
from settings import *
import time
from support import *
from timer import Timer
from inventory import Stack
from wiki import Wiki
from overlay import Overlay

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer):
		super().__init__(group)
		self.player_xp = 0
		self.player_level = self.get_player_level(self.player_xp)
		
		self.known_species = Stack()
		self.well_known_species = Stack()
	
		# tools
		self.available_tools = Stack()
		self.possessed_tools = Stack()		
		self.tool_index = 0
		self.selected_tool = 'glass'
		
		self.wiki = Wiki()
		self.toggle_bio_conditions = False
		
		self.overlay = Overlay(self)

		self.import_assets()
		self.status = 'right_idle'
		self.frame_index = 0

		# general setup
		self.image = self.animations[self.status][self.frame_index]
		self.rect = self.image.get_rect(center = pos)
		self.z = LAYERS['main']

		# movement attributes
		self.direction = pygame.math.Vector2()
		self.pos = pygame.math.Vector2(self.rect.center)
		self.speed = 150		

		# collision
		self.hitbox = self.rect.copy().inflate((-126,-70))
		self.collision_sprites = collision_sprites

		# timers 
		self.timers = {
			'tool use': Timer(350,func = self.use_tool),
			'tool switch': Timer(200)
		}

		# interaction
		self.tree_sprites = tree_sprites
		self.interaction = interaction
		self.sleep = False
		self.soil_layer = soil_layer

		# sound
		self.watering = pygame.mixer.Sound('../audio/water.mp3')
		self.watering.set_volume(0.2)

		#levelup
		self.has_reached_lvl1 = False
		self.has_reached_lvl2 = False 
		self.has_reached_lvl3 = False

	def use_tool(self):
		if not self.possessed_tools.is_empty():
			if self.selected_tool == 'glass':
				print('using glass')

			if self.selected_tool == 'binoculars':
				print('using binos')

	def get_target_pos(self):
		self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

	def import_assets(self):
		self.animations = {'up': [],'down': [],'left': [],'right': [],
						   'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
						   'right_hoe':[],'left_hoe':[],'up_hoe':[],'down_hoe':[],
						   'right_axe':[],'left_axe':[],'up_axe':[],'down_axe':[],
						   'right_water':[],'left_water':[],'up_water':[],'down_water':[]}

		for animation in self.animations.keys():
			full_path = '../graphics/character/' + animation
			self.animations[animation] = import_folder(full_path)

	def animate(self,dt):
		self.frame_index += 4 * dt
		if self.frame_index >= len(self.animations[self.status]):
			self.frame_index = 0

		self.image = self.animations[self.status][int(self.frame_index)]

	def input(self):
		keys = pygame.key.get_pressed()

		if not self.timers['tool use'].active and not self.sleep:
			# directions 
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
				if keys[pygame.K_LCTRL]:
					self.speed = 300
				elif keys[pygame.K_RCTRL]:
					self.speed = 40
				else:
					self.speed = 150
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
				if keys[pygame.K_LCTRL]:
					self.speed = 300
				elif keys[pygame.K_RCTRL]:
					self.speed = 40
				else:
					self.speed = 150
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
				if keys[pygame.K_LCTRL]:
					self.speed = 300
				elif keys[pygame.K_RCTRL]:
					self.speed = 40
				else:
					self.speed = 150
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
				if keys[pygame.K_LCTRL]:
					self.speed = 300
				elif keys[pygame.K_RCTRL]:
					self.speed = 40
				else:
					self.speed = 150
			else:
				self.direction.x = 0

			#homemenu
			if pygame.key.get_pressed()[pygame.K_m]:
				self.overlay.start_time = time.time()
				self.overlay.displaying_warning = True	

			#species inventory		
			if pygame.key.get_pressed()[pygame.K_i]:
				self.overlay.displaying_species_dict = True

			#tools inventory
			if pygame.key.get_pressed()[pygame.K_t]:
				self.overlay.displaying_tools_inventory = True

			# tool use
			if keys[pygame.K_SPACE]:
				self.timers['tool use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			# change tool
			if keys[pygame.K_q] and not self.timers['tool switch'].active and not self.possessed_tools.is_empty():
				self.timers['tool switch'].activate()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < self.possessed_tools.get_size() else 0
				self.selected_tool = self.possessed_tools.return_element(self.tool_index)
	
	def get_status(self):		
		# idle
		if self.direction.magnitude() == 0:
			self.status = self.status.split('_')[0] + '_idle'

		# tool use
		'''if self.timers['tool use'].active:
			self.status = self.status.split('_')[0] + '_' + self.selected_tool
		'''

	def update_timers(self):
		for timer in self.timers.values():
			timer.update()

	def update_stacks(self):
		if self.player_level == 1:
			self.available_tools.push('glass')
		elif self.player_level == 2:
			self.available_tools.push('binoculars')

	def update_non_collisions(self):
		if not (len(pygame.sprite.spritecollide(self,self.interaction,False)) >0 and pygame.sprite.spritecollide(self,self.interaction,False)[0].name == 'Board'):
			self.overlay.displaying_board = False

		if not (len(pygame.sprite.spritecollide(self,self.interaction,False)) >0 and pygame.sprite.spritecollide(self,self.interaction,False)[0].name == 'Biologist'):
			self.overlay.colliding_bio = False	

	def collision(self, direction):
		for sprite in self.collision_sprites.sprites():
			if hasattr(sprite, 'hitbox'):
				if sprite.hitbox.colliderect(self.hitbox):
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

			if len(pygame.sprite.spritecollide(self,self.interaction,False)) >0 and pygame.sprite.spritecollide(self,self.interaction,False)[0].name == 'Board':
				self.overlay.displaying_board = True
				print('here')

			if len(pygame.sprite.spritecollide(self,self.interaction,False)) >0 and pygame.sprite.spritecollide(self,self.interaction,False)[0].name == 'Biologist':
				self.overlay.colliding_bio = True				
				self.overlay.start_time = time.time()
				self.overlay.displaying_message_bio = True

			#species
			for tile in SPECIES_TILES:
				if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == tile:
					species = SPECIES[SPECIES_TILES.index(tile)]
					if not (self.known_species.is_here(species)):
						self.player_xp +=10
						self.known_species.push(species)
						self.overlay.popup_name = species
						self.overlay.start_time = time.time()
						self.overlay.displaying_popup_new_species = True		
					
	def move(self,dt):

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

	def update(self, dt):
		self.player_level = self.get_player_level(self.player_xp)
		self.input()
		self.get_status()
		self.update_timers()
		self.update_stacks()
		self.get_target_pos()

		self.move(dt)
		self.animate(dt)

	def get_player_level(self, xp):
		if 0<=xp<100:
			return 0
		elif 100<=xp<200:
			return 1
		else:
			return 2

		

