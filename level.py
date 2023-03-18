import pygame 
from settings import *
from player import Player
from animal import Animal
from overlay import Overlay
from sprites import Generic, Water, Species, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint

class Level:
	def __init__(self):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()

		#animals sprite groups
		self.animal_collision_sprites = pygame.sprite.Group()

		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites, self.animal_collision_sprites)
		self.setup()
		self.overlay = Overlay(self.player)
		self.transition = Transition(self.reset, self.player)

		# sky
		self.rain = Rain(self.all_sprites)
		self.raining = randint(0,10) > 7
		self.soil_layer.raining = self.raining
		self.sky = Sky(self.overlay)

		# music
		self.success = pygame.mixer.Sound('../audio/success.wav')
		self.success.set_volume(0.3)
		self.music = pygame.mixer.Sound('../audio/music.mp3')
		self.music.set_volume(0)
		self.music.play(loops = -1)

	def setup(self):
		tmx_data = load_pygame('../data/map3.tmx') 
		# Fence
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x * TILE_SIZE,y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites, self.animal_collision_sprites])

		# water 
		water_frames = import_folder('../graphics/water')
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x * TILE_SIZE,y * TILE_SIZE), water_frames, self.all_sprites)

		# trees 
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y), 
				surf = obj.image, 
				groups = [self.all_sprites, self.collision_sprites, self.animal_collision_sprites, self.tree_sprites], 
				name = obj.name,
				player_add = self.player_add)

		# collision tiles
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), groups = [self.collision_sprites, self.animal_collision_sprites])

		# Player and animals
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y), 
					group = self.all_sprites, 
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer)

			for tile in SPECIES_TILES:
				if obj.name == tile:
					Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name =='Frog':
				self.frog = Animal(
					name = 'frog',
					pos = (obj.x, obj.y),
					groups = [self.all_sprites, self.collision_sprites],
					player = self.player,
					animal_collision_sprites = self.animal_collision_sprites)
				self.frog_collision = Generic(self.frog.pos, pygame.Surface((21,16)), self.collision_sprites)

			Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)


		Generic(
			pos = (0,0),
			surf = pygame.image.load('../graphics/world/ground2.png').convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def update_animal_collision(self):
		#Generic(self.frog.pos, pygame.Surface((21,16)), self.collision_sprites)
		self.frog_collision.pos = self.frog.pos

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

	def run(self,dt):		
		# drawing logic
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)

		# animals
		
		
		# updates
		self.all_sprites.update(dt)
		self.player.update_non_collisions()
		self.update_animal_collision()

		# overlay
		self.overlay.run(dt)

		# weather
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