import pygame 
from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, Species, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint
from menu2 import Menu2

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()

		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.reset, self.player)

		# sky
		self.rain = Rain(self.all_sprites)
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		self.sky = Sky()

		# shop
		#self.menu = Menu(self.player, self.toggle_shop)
		#self.shop_active = False

		#biologist species menu
		#self.bio_species = Menu2(self.player)


		# music
		self.success = pygame.mixer.Sound('../audio/success.wav')
		self.success.set_volume(0.3)
		self.music = pygame.mixer.Sound('../audio/music.mp3')
		self.music.set_volume(0)
		self.music.play(loops = -1)

	def setup(self):
		tmx_data = load_pygame('../data/map3.tmx')
		'''
		if player.player_level == 0:
			tmx_data = load_pygame('../data/map3_lvl0.tmx')
		
		if player.player_level == 1:
			tmx_data = load_pygame('../data/map3_lvl1.tmx')

		if player.player_level == 2:
			tmx_data = load_pygame('../data/map3_lvl2.tmx')'''

		# Fence
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

		# water 
		water_frames = import_folder('../graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

		# trees 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)

		# species 
		'''
		for obj in tmx_data.get_layer_by_name('Species'):
			Species((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])
		'''

		# collision tiles
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites)

		# Player 
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), 
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer
					)
					
			if obj.name == 'Board':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Biologist':
				Interaction((obj.x,obj.y), (obj.width,obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Double_mushroom':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Small':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Large':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
			
			if obj.name == 'Bush':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Sunflower':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Pink_flower':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Blue_flower':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'One_purple_mushroom':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Two_purple_mushrooms':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
				
			if obj.name == 'One_red_mushroom':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
				
			if obj.name == 'Two_red_mushrooms':
				Interaction((obj.x,obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/ground2.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def player_add(self,item):
		self.player.item_inventory[item] += 1
		self.success.play()

	def reset(self):
		# soil
		self.soil_layer.remove_water()
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		if self.raining:
			self.soil_layer.water_all()

		# sky
		self.sky.start_color = [255,255,255]

	def plant_collision(self):
		if self.soil_layer.plant_sprites:
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(plant.rect.topleft, plant.image, self.all_sprites, z = LAYERS['main'])
					self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

	def run(self,dt):		
		# drawing logic
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)
		
		# updates
		self.all_sprites.update(dt)
		self.plant_collision()

		# weather
		self.overlay.display(self.player.player_xp)
		self.overlay.display_keys()
		if self.raining:
			self.rain.update()
		self.sky.display(dt)

		# transition overlay
		if self.player.sleep:
			self.transition.play()

class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values():
			for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)

					# # anaytics
					# if sprite == player:
					# 	pygame.draw.rect(self.display_surface,'red',offset_rect,5)
					# 	hitbox_rect = player.hitbox.copy()
					# 	hitbox_rect.center = offset_rect.center
					# 	pygame.draw.rect(self.display_surface,'green',hitbox_rect,5)
					# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
					# 	pygame.draw.circle(self.display_surface,'blue',target_pos,5)