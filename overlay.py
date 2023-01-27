import sys
import pygame
from settings import *

class Overlay:
	def __init__(self,player):

		# general setup
		self.display_surface = pygame.display.get_surface()
		self.player = player

		# imports 
		overlay_path = '../graphics/overlay/'
		self.tools_surf = {tool: pygame.image.load(f'{overlay_path}{tool}.png').convert_alpha() for tool in TOOLS}
		#self.seeds_surf = {seed: pygame.image.load(f'{overlay_path}{seed}.png').convert_alpha() for seed in player.seeds}
		self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
		self.font_mid = pygame.font.Font('../font/LycheeSoda.ttf', 50)
		self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
		self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 15)

		self.display_keys_shortcuts = True

	def display(self, xp):
		lvl = self.player.get_player_level(xp)

		# tool
		if not self.player.possessed_tools.is_empty():
			tool_surf = self.tools_surf[self.player.selected_tool]
			tool_rect = tool_surf.get_rect(midbottom = OVERLAY_POSITIONS['tool'])
			self.display_surface.blit(tool_surf,tool_rect)

		#xp and level
		xp_txt_surf = self.font_small.render('  '+str(xp)+' XP  ', False, 'White')
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

		background_rect = pygame.Rect(lvl_txt_rect.x, lvl_txt_rect.y, xp_txt_rect.width+40, xp_txt_rect.height + lvl_txt_rect.height)
		pygame.draw.rect(self.display_surface, color,background_rect, border_top_left_radius = 5)
		self.display_surface.blit(xp_txt_surf, xp_txt_rect)
		self.display_surface.blit(lvl_txt_surf, lvl_txt_rect)

	def display_interaction_options(self):
		pygame.draw.rect(self.display_surface, 'White', pygame.Rect(150, 640, 1240, 640))
		possible_interactions_surf = self.font_small.render('Interact >', False, 'Black')
		possible_interactions_rect = possible_interactions_surf.get_rect(topleft = (160, 685))
		self.display_surface.blit(possible_interactions_surf, possible_interactions_rect)
	
	def display_keys(self):
		reveal_title_surf = self.font_smaller.render('Show key shortcuts >', False,'White')
		reveal_title_rect = reveal_title_surf.get_rect(topright = (1270,5))
		
		box_title_surf = self.font_small.render('Keys shortcuts:', False, 'White')
		box_title_rect = box_title_surf.get_rect(topleft = (980, 10))

		exit_cross_surf = self.font_small.render('[x]', False, 'White')
		exit_cross_rect = exit_cross_surf.get_rect(topright = (1270,10))

		keys_strg = ['Press i to view your Species Dictionary',
					'Press t to view your tools',
					'Press SPACE to use your active tool',
					'Press q to change your active tool', 
					'Press m to return to the homemenu']

		#hover animation
		mouse_pos = pygame.mouse.get_pos()

		#display
		if not self.display_keys_shortcuts:
			pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(1130, 0, 150, 28), border_bottom_left_radius=10)
			#hover animation
			mouse_pos = pygame.mouse.get_pos()
			if reveal_title_rect.collidepoint(mouse_pos):
				reveal_title_surf = self.font_smaller.render('Show key shortcuts >', False,'Black')

			self.display_surface.blit(reveal_title_surf, reveal_title_rect)			

		if self.display_keys_shortcuts:
			pygame.draw.rect(self.display_surface, 'Grey', pygame.Rect(960, 0, 480, 140), border_bottom_left_radius=10)
			#hover animation
			if exit_cross_rect.collidepoint(mouse_pos):
				exit_cross_surf = self.font_small.render('[x]', False, 'Black')

			self.display_surface.blit(box_title_surf, box_title_rect)
			self.display_surface.blit(exit_cross_surf, exit_cross_rect)
			for i in range(0,len(keys_strg)):
				height = 27 + (i+1)*17
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
					self.display_keys_shortcuts = False
				
				if reveal_title_rect.collidepoint(x,y): #isn't perfect but it works
					self.display_keys_shortcuts = True
