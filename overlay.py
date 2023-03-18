import sys
import time
import pygame
from settings import *

from board import Board
from toggle import Toggle
from inventory import EquipmentInventory, SpeciesDictionary
from intromenu import Intromenu
from popup import PopUp

class Overlay:
	def __init__(self,player):

		# general setup
		self.display_surface = pygame.display.get_surface()
		self.player = player
		self.start_time = 0
		self.pos = 0

		# imports 
		overlay_path = '../graphics/overlay/'
		self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in TOOLS}
		self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
		self.font_mid = pygame.font.Font('../font/LycheeSoda.ttf', 50)
		self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
		self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 15)

		#instances
		self.board = Board(self.player)
		self.toggle_bio_species = Toggle()
		self.tools_inventory = EquipmentInventory(self.player.available_tools, self.player.possessed_tools)
		self.dictionary_species = SpeciesDictionary(self.player.wiki)

		#instances of popups
		self.popup_name = ''

		#STATUS
		self.displaying_keys_shortcuts = True
		self.displaying_toggle = False
		self.colliding_bio = False
		self.displaying_lvl_xp = True
		self.displaying_popup_new_species = False
		self.displaying_warning = False
		self.displaying_message_bio = False
		self.displaying_getting_dark = False

		self.displaying_board = False
		self.displaying_tools_inventory = False
		self.displaying_species_dict = False

	def run(self, dt):
		self.display_shortcuts()

		if self.displaying_getting_dark and not self.player.overlay.displaying_popup_new_species:
			self.display_getting_dark()

		if self.player.overlay.displaying_warning and not pygame.key.get_pressed()[pygame.K_ESCAPE]:
			if self.pos < 260:
				self.pos += 1000*dt	
				self.warning_block(self.pos)
			else:
				self.warning_block(260)
		
		if self.player.overlay.displaying_warning and pygame.key.get_pressed()[pygame.K_ESCAPE]:
			self.close_warning_block(dt)

		if self.player.overlay.displaying_message_bio and not self.player.overlay.displaying_toggle and not self.displaying_getting_dark:
			self.display_message_bio()

		if self.player.overlay.displaying_popup_new_species and not self.player.overlay.displaying_message_bio:
			self.display_popup_new_species(self.player.overlay.popup_name+'  ')

		if pygame.key.get_pressed()[pygame.K_RETURN] and self.player.overlay.colliding_bio :
			self.player.overlay.displaying_toggle = True

		if pygame.key.get_pressed()[pygame.K_ESCAPE] and self.displaying_toggle:
			self.player.overlay.displaying_toggle = False

		if self.displaying_lvl_xp and not self.player.overlay.displaying_board:
			self.display_lvl_xp_tool_icon()

		if self.player.overlay.displaying_tools_inventory:
			self.player.overlay.displaying_keys_shortcuts = False
			self.display_tools_inventory()

		if self.player.overlay.displaying_tools_inventory and pygame.key.get_pressed()[pygame.K_q]:
			self.tools_inventory.in_inventory_menu = False
			self.player.overlay.displaying_tools_inventory = False

		if self.player.overlay.displaying_species_dict:
			self.player.overlay.displaying_keys_shortcuts = False
			self.display_species_dict()

		if self.player.overlay.displaying_species_dict and pygame.key.get_pressed()[pygame.K_q]:
			self.dictionary_species.in_inventory_menu = False
			self.player.overlay.displaying_species_dict= False

		if self.player.overlay.displaying_toggle and not(self.player.overlay.displaying_warning):
			self.display_toggle()

		if self.player.overlay.displaying_board and not(self.player.overlay.displaying_tools_inventory or self.player.overlay.displaying_species_dict):
			self.player.overlay.displaying_keys_shortcuts = False
			self.board.run(self.player.available_tools, self.player.possessed_tools)

	def display_tools_inventory(self):		
		self.tools_inventory.in_inventory_menu = True
		self.tools_inventory.display_inventory_menu(self.player.possessed_tools.get_size())

	def display_species_dict(self):		
		self.dictionary_species.in_inventory_menu = True
		self.dictionary_species.display_inventory_menu(self.player.known_species, self.player.well_known_species, self.player.player_xp)

	def display_lvl_xp_tool_icon(self):
		lvl = self.player.get_player_level(self.player.player_xp)

		# tool
		if not self.player.possessed_tools.is_empty():
			tool_surf = self.tools_surf[self.player.selected_tool]
			tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
			self.display_surface.blit(tool_surf,tool_rect)

		#xp and level
		xp_txt_surf = self.font_small.render('  '+str(self.player.player_xp)+' XP  ', False, 'White')
		xp_txt_rect = xp_txt_surf.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT))
		lvl_txt_surf = self.font_small.render('  Level '+str(lvl)+'  ', False, 'White')
		lvl_txt_rect = lvl_txt_surf.get_rect(bottomright=(SCREEN_WIDTH, SCREEN_HEIGHT-30))

		#background color change
		if lvl == 0:
			color = MIDGREEN
		elif lvl == 1:
			color = 'chartreuse3'
		else:
			color = 'cornflowerblue'

		if self.displaying_lvl_xp:
			background_rect = pygame.Rect(lvl_txt_rect.x, lvl_txt_rect.y, xp_txt_rect.width+40, xp_txt_rect.height + lvl_txt_rect.height)
			pygame.draw.rect(self.display_surface, color,background_rect, border_top_left_radius = 5)
			self.display_surface.blit(xp_txt_surf, xp_txt_rect)
			self.display_surface.blit(lvl_txt_surf, lvl_txt_rect)

	def display_shortcuts(self):
		reveal_title_surf = self.font_smaller.render('Show key shortcuts >', False,'White')
		reveal_title_rect = reveal_title_surf.get_rect(topright = (1270,5))
		
		box_title_surf = self.font_small.render('Keys shortcuts:', False, 'White')
		box_title_rect = box_title_surf.get_rect(topleft = (980, 8))

		exit_cross_surf = self.font_small.render('[x]', False, 'White')
		exit_cross_rect = exit_cross_surf.get_rect(topright = (1270,10))

		keys_strg = ['Press i to view your Species Dictionary',
					'Press t to view your tools',
					'Press SPACE to use your active tool',
					'Press q to change your active tool', 
					'Press m to return to the homemenu',
					'Press Left Control to run',
					'Press Right Control to walk slowly']

		#hover animation
		mouse_pos = pygame.mouse.get_pos()

		#display
		if not self.displaying_keys_shortcuts:
			pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(1130, 0, 150, 28), border_bottom_left_radius=10)
			#hover animation
			mouse_pos = pygame.mouse.get_pos()
			if reveal_title_rect.collidepoint(mouse_pos):
				reveal_title_surf = self.font_smaller.render('Show key shortcuts >', False,'Black')

			self.display_surface.blit(reveal_title_surf, reveal_title_rect)			

		if self.displaying_keys_shortcuts:
			pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(960, 0, 480, 170), border_bottom_left_radius=10)
			#hover animation
			if exit_cross_rect.collidepoint(mouse_pos):
				exit_cross_surf = self.font_small.render('[x]', False, 'Black')

			self.display_surface.blit(box_title_surf, box_title_rect)
			self.display_surface.blit(exit_cross_surf, exit_cross_rect)
			for i in range(0,len(keys_strg)):
				height = 24 + (i+1)*17
				key_surf = self.font_smaller.render(keys_strg[i], False, 'White')
				key_rect = key_surf.get_rect(topleft=(980, height))
				self.display_surface.blit(key_surf, key_rect)

		#user interaction
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				x,y = event.pos
				if exit_cross_rect.collidepoint(x,y):
					self.displaying_keys_shortcuts = False
				
				if reveal_title_rect.collidepoint(x,y): #isn't perfect but it works
					self.displaying_keys_shortcuts = True

	def display_toggle(self):		
		if self.player.overlay.colliding_bio:
			self.toggle_bio_species.in_menu = True
			self.toggle_bio_species.display_menu(self.player.known_species, self.player.well_known_species)

			if len(pygame.sprite.spritecollide(self.player, self.player.interaction, False)) == 0:
				self.player.toggle_bio_conditions = False

			elif (not 'Biologist' in pygame.sprite.spritecollide(self.player,self.player.interaction,False)[0].name):
				self.player.toggle_bio_conditions = False

	def display_popup_new_species(self, species):
		popup = PopUp(species, first_encounter = True)
		if time.time() -self.player.overlay.start_time <= 3:
			popup.display()
		else:
			popup.first_encounter = False
			self.player.overlay.displaying_popup_new_species = False

	def warning_block(self, x):
		warning1_txt_surf = self.font_small.render('Are you sure you', False, 'Black')
		warning2_txt_surf = self.font_small.render('want to return to', False, 'Black')
		warning3_txt_surf = self.font_small.render('the homescreen ?', False, 'Black')
		warning1_txt_rect = warning1_txt_surf.get_rect(center = (-145 + x, 300))
		warning2_txt_rect = warning2_txt_surf.get_rect(center = (-145 + x, 350))
		warning3_txt_rect = warning3_txt_surf.get_rect(center = (-145 + x, 400))
		exit_surf = self.font_smaller.render('Press ESC to close', False, 'Black')
		exit_rect = exit_surf.get_rect(center = (-145 + x, 550))


		#button
		yes_surf = self.font_small.render('  yes  ', False, 'White')
		yes_rect = yes_surf.get_rect(center = (-145 + x, 480))
		mouse_pos = pygame.mouse.get_pos()

		#display
		pygame.draw.rect(self.display_surface, 'White', pygame.Rect(-270 + x, 200, 260, 400), border_radius = 5)
		pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(-270 + x, 210, 250, 380), width =5, border_radius = 5)
		pygame.draw.rect(self.display_surface, 'Black', yes_rect, border_radius = 10)

		if yes_rect.collidepoint(mouse_pos):
			pygame.draw.rect(self.display_surface, 'chartreuse3', yes_rect, border_radius = 10)
			yes_surf = self.font_small.render('  yes  ', False, 'White')
			yes_rect = yes_surf.get_rect(center = (-145 + x, 480))

		self.display_surface.blit(warning1_txt_surf, warning1_txt_rect)
		self.display_surface.blit(warning2_txt_surf, warning2_txt_rect)
		self.display_surface.blit(warning3_txt_surf, warning3_txt_rect)
		self.display_surface.blit(yes_surf, yes_rect)
		self.display_surface.blit(exit_surf, exit_rect)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if yes_rect.collidepoint(mouse_pos):
					self.player.overlay.displaying_warning = False
					intromenu = Intromenu()
					intromenu.run()

	def close_warning_block(self, dt):
		self.pos -= 800*dt
		self.warning_block(self.pos)
		if self.pos <= 20:
			self.player.overlay.displaying_warning =  False

	def display_message_bio(self):
		if time.time() - self.player.overlay.start_time <= 5:
			#text overlay
			strg_list = ['  Congratulations! You have found a wild biologist !  ',
						'  You can ask them questions about a species you have discovered ',
						'  To do so press the ENTER key  ']

			txt = self.font_small.render(strg_list[1], False, 'Black').get_rect(midtop = (640, 30))
			box = pygame.Rect(txt.x, 0, txt.width, 90)
			pygame.draw.rect(self.display_surface, 'White', box, border_bottom_left_radius=10, border_bottom_right_radius=10)

			for strg in strg_list:
				txt_surf = self.font_small.render(strg, False, 'Black')
				txt_rect = txt_surf.get_rect(midtop = (640, 0+30*strg_list.index(strg)))

				#display
				self.display_surface.blit(txt_surf, txt_rect)

	def display_getting_dark(self):
		text_surf = self.font_small.render('  it is getting dark, you should go to the board  ', False, 'Black')
		text_rect = text_surf.get_rect(center = (640, 15))
		pygame.draw.rect(self.display_surface, 'Grey', text_rect, border_bottom_left_radius=10, border_bottom_right_radius=10)
		self.display_surface.blit(text_surf, text_rect)
