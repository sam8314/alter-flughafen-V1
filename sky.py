import pygame 
from settings import *
from support import import_folder
from sprites import Generic
from random import randint, choice

class Sky:
<<<<<<< HEAD
	def __init__(self, overlay):
=======
	def __init__(self):
>>>>>>> b714464edd93ff01282798143cc34c210bb49cbf
		self.display_surface = pygame.display.get_surface()
		self.full_surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
		self.start_color = [255,255,255]
		self.end_color = (38,101,189)
<<<<<<< HEAD
		self.overlay = overlay
		self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)

=======
		self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)

	def display_popup(self):
		text_surf = self.font_small.render('  it is getting dark, you should go to the board  ', False, 'Black')
		text_rect = text_surf.get_rect(center = (640, 15))
		pygame.draw.rect(self.display_surface, 'Grey', text_rect, border_bottom_left_radius=10, border_bottom_right_radius=10)
		self.display_surface.blit(text_surf, text_rect)

>>>>>>> b714464edd93ff01282798143cc34c210bb49cbf
	def display(self, dt):
		for index, value in enumerate(self.end_color):
			if self.start_color[index] > value:
				self.start_color[index] -= 1.2 * dt

		self.full_surf.fill(self.start_color)
		self.display_surface.blit(self.full_surf, (0,0), special_flags = pygame.BLEND_RGBA_MULT)

		if self.start_color[0]<130:
<<<<<<< HEAD
			self.overlay.displaying_getting_dark = True
=======
			self.display_popup()
>>>>>>> b714464edd93ff01282798143cc34c210bb49cbf

class Drop(Generic):
	def __init__(self, surf, pos, moving, groups, z):
		
		# general setup
		super().__init__(pos, surf, groups, z)
		self.lifetime = randint(400,500)
		self.start_time = pygame.time.get_ticks()

		# moving 
		self.moving = moving
		if self.moving:
			self.pos = pygame.math.Vector2(self.rect.topleft)
			self.direction = pygame.math.Vector2(-2,4)
			self.speed = randint(200,250)

	def update(self,dt):
		# movement
		if self.moving:
			self.pos += self.direction * self.speed * dt
			self.rect.topleft = (round(self.pos.x), round(self.pos.y))

		# timer
		if pygame.time.get_ticks() - self.start_time >= self.lifetime:
			self.kill()

class Rain:
	def __init__(self, all_sprites):
		self.all_sprites = all_sprites
		self.rain_drops = import_folder('../graphics/rain/drops/')
		self.rain_floor = import_folder('../graphics/rain/floor/')
		self.floor_w, self.floor_h =  pygame.image.load('../graphics/world/ground2.png').get_size()

	def create_floor(self):
		Drop(
			surf = choice(self.rain_floor), 
			pos = (randint(0,self.floor_w),randint(0,self.floor_h)), 
			moving = False, 
			groups = self.all_sprites, 
			z = LAYERS['rain floor'])

	def create_drops(self):
		Drop(
			surf = choice(self.rain_drops), 
			pos = (randint(0,self.floor_w),randint(0,self.floor_h)), 
			moving = True, 
			groups = self.all_sprites, 
			z = LAYERS['rain drops'])

	def update(self):
		self.create_floor()
		self.create_drops()