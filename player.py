import pygame
from settings import *
from support import *
from timer import Timer
from inventory import DisplayInventory, EquipmentInventory, Stack2
from action import Action
from menu2 import Menu2
from wiki import Wiki
from board import Board

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer):
		super().__init__(group)
		self.player_xp = 0
		self.player_level = self.get_player_level(self.player_xp)
		
		self.known_species = Stack2()
		self.well_known_species = Stack2()

		self.available_tools = Stack2()
		self.possessed_tools = Stack2()
		
		self.toggle_bio_species = Menu2()
		self.toggle_bio_conditions = False
		self.wiki = Wiki()

		self.dictionary_species = DisplayInventory(self.wiki)
		self.tools_inventory = EquipmentInventory(self.available_tools, self.possessed_tools)
		self.board = Board(self)

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
		self.speed = 200		

		# collision
		self.hitbox = self.rect.copy().inflate((-126,-70))
		self.collision_sprites = collision_sprites

		#actions
		self.encountered_board = Action()
		self.encountered_biologist = Action()
		self.encountered_new_small = Action() #small tree
		self.encountered_new_large = Action() #large tree
		self.encountered_new_bush = Action()
		self.encountered_new_sunflower = Action()
		self.encountered_new_pink_flower = Action()
		self.encountered_new_blue_flower = Action()
		self.encountered_new_single_purple_mushroom = Action()
		self.encountered_new_pair_purple_mushrooms = Action()
		self.encountered_new_single_red_mushroom = Action()
		self.encountered_new_pair_red_mushrooms = Action()

		#homemenu overlay
		self.homemenu = Action()

		# timers 
		self.timers = {
			'warning homescreen' : Timer(4000, activefunc=self.homemenu.display_warning),
			'tool use': Timer(350,func = self.use_tool),
			'tool switch': Timer(200),
			'popup message board': Timer(1300,activefunc= self.encountered_board.display_board_message),
			'popup message new small tree': Timer(1200, activefunc = self.encountered_new_small.display_small_tree),
			'popup message new large tree': Timer(1200, activefunc = self.encountered_new_large.display_large_tree),
			'popup message new bush': Timer(1200, activefunc = self.encountered_new_bush.display_bush),
			'popup message new sunflower': Timer(1200, activefunc = self.encountered_new_sunflower.display_sunflower),
			'popup message new pink flower': Timer(1200, activefunc = self.encountered_new_pink_flower.display_pink_flower),
			'popup message new blue flower': Timer(1200, activefunc = self.encountered_new_blue_flower.display_blue_flower),
			'popup message new single purple mushroom': Timer(1200, activefunc = self.encountered_new_single_purple_mushroom.display_one_purple_mushroom),
			'popup message new pair purple mushrooms': Timer(1200, activefunc = self.encountered_new_pair_purple_mushrooms.display_two_purple_mushrooms),
			'popup message new single red mushroom': Timer(1200, activefunc = self.encountered_new_single_red_mushroom.display_one_red_mushroom),
			'popup message new pair red mushrooms': Timer(1200, activefunc = self.encountered_new_pair_red_mushrooms.display_two_red_mushrooms),
			'popup message biologist': Timer(1300, activefunc=self.encountered_biologist.display_message_bio)
		}

		# tools 
		if not self.possessed_tools.is_empty():
			self.tool_index = 0
			self.selected_tool = self.possessed_tools.return_element(self.tool_index)

		# interaction
		self.tree_sprites = tree_sprites
		self.interaction = interaction
		self.sleep = False
		self.soil_layer = soil_layer

		# sound
		self.watering = pygame.mixer.Sound('../audio/water.mp3')
		self.watering.set_volume(0.2)

	def use_tool(self):
		if self.selected_tool == 'glass':
			print('using glass')

		if self.selected_tool == 'binoculars':
			print('using binos')

	def get_target_pos(self):

		self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]]

	def use_seed(self):
		'''
		if self.seed_inventory[self.selected_seed] > 0:
			self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
			self.seed_inventory[self.selected_seed] -= 1
		'''

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
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_RIGHT]:
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT]:
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0

			#homemenu
			if pygame.key.get_pressed()[pygame.K_m]:
				self.timers['warning homescreen'].activate()

			#species inventory		
			if pygame.key.get_pressed()[pygame.K_i]:
				self.dictionary_species.in_inventory_menu = True
				self.dictionary_species.display_inventory_menu(self.known_species, self.well_known_species, self.player_xp)

			#tools inventory
			if pygame.key.get_pressed()[pygame.K_t]:
				self.tools_inventory.in_inventory_menu = True
				self.tools_inventory.display_inventory_menu(self.possessed_tools.get_size())

			# tool use
			if keys[pygame.K_SPACE]:
				self.timers['tool use'].activate()
				self.direction = pygame.math.Vector2()
				self.frame_index = 0

			# change tool
			if keys[pygame.K_q] and not self.timers['tool switch'].active:
				self.timers['tool switch'].activate()
				self.tool_index += 1
				self.tool_index = self.tool_index if self.tool_index < self.possessed_tools.get_size() else 0
				self.selected_tool = self.possessed_tools.return_element(self.tool_index)

			if keys[pygame.K_RETURN]:
				collided_interaction_sprite = pygame.sprite.spritecollide(self,self.interaction,False)
				if collided_interaction_sprite:
					if collided_interaction_sprite[0].name == 'Biologist':
						self.toggle_bio_conditions = True
					elif collided_interaction_sprite[0].name == 'Board':
						self.board.run()

			if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.toggle_bio_conditions:
				self.toggle_bio_conditions = False
	
	def display_toggle_bio_species(self):		
		if self.toggle_bio_conditions:
			self.toggle_bio_species.in_menu = True
			self.toggle_bio_species.display_menu(self.known_species, self.well_known_species)

			if len(pygame.sprite.spritecollide(self, self.interaction, False)) == 0:
				self.toggle_bio_conditions = False

			elif (not 'Biologist' in pygame.sprite.spritecollide(self,self.interaction,False)[0].name):
				self.toggle_bio_conditions = False

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
				#self.timers['popup message board'].activate()
				self.board.run()

			if len(pygame.sprite.spritecollide(self,self.interaction,False)) >0 and pygame.sprite.spritecollide(self,self.interaction,False)[0].name == 'Biologist':
				if not self.toggle_bio_species.in_menu:
					self.timers['popup message biologist'].activate()	

			#trees
			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'Small':
				if not (self.known_species.is_here('small_tree')):
					self.player_xp +=10
					self.known_species.push('small_tree')
					self.timers['popup message new small tree'].activate()
					self.encountered_new_small.first_encounter = False

			if len(pygame.sprite.spritecollide(self,self.interaction,False)) >0 and pygame.sprite.spritecollide(self,self.interaction,False)[0].name == 'Large':				
				if not (self.known_species.is_here('large_tree')):
					self.player_xp +=10
					self.known_species.push('large_tree')
					self.timers['popup message new large tree'].activate()
					self.encountered_new_large.first_encounter = False

			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'Bush':				
				if not (self.known_species.is_here('bush')):
					self.player_xp +=10
					self.known_species.push('bush')
					self.timers['popup message new bush'].activate()
					self.encountered_new_bush.first_encounter = False
			
			#species
			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'Sunflower':
				if not (self.known_species.is_here('sunflower')):
					self.player_xp +=10
					self.known_species.push('sunflower')
					self.timers['popup message new sunflower'].activate()
					self.encountered_new_sunflower.first_encounter = False
				
			
			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'Pink_flower':
				if not (self.known_species.is_here('pink_flower')):
					self.player_xp +=10
					self.known_species.push('pink_flower')
					self.timers['popup message new pink flower'].activate()
					self.encountered_new_pink_flower.first_encounter = False

			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'Blue_flower':
				if not (self.known_species.is_here('blue_flower')):
					self.player_xp +=10
					self.known_species.push('blue_flower')
					self.timers['popup message new blue flower'].activate()
					self.encountered_new_blue_flower.first_encounter = False

			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'One_purple_mushroom':
				if not (self.known_species.is_here('single_purple_mushroom')):
					self.player_xp +=10
					self.known_species.push('single_purple_mushroom')
					self.timers['popup message new single purple mushroom'].activate()
					self.encountered_new_single_purple_mushroom.first_encounter = False
			
			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'Two_purple_mushrooms':
				if not (self.known_species.is_here('pair_purple_mushrooms')):
					self.player_xp +=10
					self.known_species.push('pair_purple_mushrooms')
					self.timers['popup message new pair purple mushrooms'].activate()
					self.encountered_new_pair_purple_mushrooms.first_encounter = False
			
			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'One_red_mushroom':
				if not (self.known_species.is_here('single_red_mushroom')):
					self.player_xp +=10
					self.known_species.push('single_red_mushroom')
					self.timers['popup message new single red mushroom'].activate()
					self.encountered_new_single_red_mushroom.first_encounter = False
			
			if len(pygame.sprite.spritecollide(self, self.interaction, False)) >0 and pygame.sprite.spritecollide(self,self.interaction, False)[0].name == 'Two_red_mushrooms':
				if not (self.known_species.is_here('pair_red_mushrooms')):
					self.player_xp +=10
					self.known_species.push('pair_red_mushrooms')
					self.timers['popup message new pair red mushrooms'].activate()
					self.encountered_new_pair_purple_mushrooms.first_encounter = False		
					
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
		self.get_target_pos()
		self.display_toggle_bio_species()

		self.move(dt)
		self.animate(dt)

	def get_player_level(self, xp):
		if 0<=xp<100:
			return 0
		elif 100<=xp<200:
			return 1
		else:
			return 2

