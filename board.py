import sys
<<<<<<< HEAD
import pygame
import time
=======
import pygame 
from timer import Timer
>>>>>>> b714464edd93ff01282798143cc34c210bb49cbf
from settings import *

class Board(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = pygame.display.get_surface()
        self.in_board = True 
        self.hasnt_been_board = True
        self.player = player
<<<<<<< HEAD
        self.selected_tool = None
        self.clicking_new_day = False

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 25)

    def run(self, available_tools, possessed_tools):
        self.hasnt_been_board = False

        start = time.time()
        if time.time()-start <= 1300:
            self.display_board(available_tools, possessed_tools)
            self.input()

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_RETURN] or (event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(160, 210, 240, 380).collidepoint(mouse_pos)):
=======

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 20)

    def run(self):
        self.hasnt_been_board = False
        timer = Timer(1300, activefunc = self.display_board)
        timer.activate()
        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_RETURN]:
>>>>>>> b714464edd93ff01282798143cc34c210bb49cbf
                self.player.status = 'up_idle'
                self.player.sleep = True
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
<<<<<<< HEAD
            if not(self.player.available_tools.is_empty()) and (event.type == pygame.MOUSEBUTTONDOWN and pygame.Rect(700, 250, 420, 45).collidepoint(mouse_pos)):
                if not self.player.possessed_tools.is_here(self.player.available_tools.peek()):
                    self.player.possessed_tools.push(self.player.available_tools.pop())

    def display_board(self, available_tools, possessed_tools):
        #background
        pygame.draw.rect(self.display_surface, 'bisque3', pygame.Rect(100, 100, 1080, 560), border_radius=20)#big background
        pygame.draw.rect(self.display_surface, 'azure4', pygame.Rect(70, 70, 1140, 720), width = 15, border_radius=20)#metal bar
        pygame.draw.rect(self.display_surface, 'azure3', pygame.Rect(80, 80, 1120, 730), width = 7, border_radius=20)#shine

        #text
        title_surf = self.font_big.render('Alter Flugplatz Karlsruhe', False, 'aquamarine4')
        title_rect = title_surf.get_rect(topleft = (120, 110))
        self.display_surface.blit(title_surf, title_rect)

        #NEW DAY button
        box = pygame.Rect(160, 210, 240, 380)
    
        if box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.display_surface, 'azure3', box, border_radius=10)
        else:
            pygame.draw.rect(self.display_surface, 'azure2', box, border_radius=10)

        sun_surf = pygame.image.load('../graphics/menu/sun.png').convert_alpha()
        sun_surf = pygame.transform.rotozoom(sun_surf, 0, 3)
        sun_rect = sun_surf.get_rect(center = box.center)
        sun_txt_surf1 = self.font_smaller.render(' Press ENTER', False, 'aquamarine4')
        sun_txt_rect1 = sun_txt_surf1.get_rect(center = (box.centerx, box.centery + 130))
        sun_txt_surf2 = self.font_smaller.render('to start a new day', False, 'aquamarine4')
        sun_txt_rect2 = sun_txt_surf2.get_rect(center = (box.centerx, box.centery + 150))
        self.display_surface.blit(sun_surf, sun_rect)
        self.display_surface.blit(sun_txt_surf1, sun_txt_rect1)
        self.display_surface.blit(sun_txt_surf2, sun_txt_rect2)

        
        #MINIMAP button
        box = pygame.Rect(430, 210, 240, 380)
        if box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(self.display_surface, 'azure3', box, border_radius=10)
        else:
            pygame.draw.rect(self.display_surface, 'azure2', box, border_radius=10)
        map_surf = pygame.image.load('../graphics/menu/map.png').convert_alpha()
        map_surf = pygame.transform.rotozoom(map_surf, 0, 1.9)
        map_rect = map_surf.get_rect(center = box.center)
        map_txt_surf = self.font_smaller.render('see the minimap', False, 'aquamarine4')
        map_txt_rect = map_txt_surf.get_rect(center = (box.centerx, box.centery + 150))
        self.display_surface.blit(map_surf, map_rect)
        self.display_surface.blit(map_txt_surf, map_txt_rect)

        #EQUIPMENT buttons
        box1 = pygame.Rect(700, 250, 420, 45)
        pygame.draw.rect(self.display_surface, 'azure3', box1, border_radius=10)

        if available_tools.is_empty():
            equip_txt_surf = self.font_small.render('levelup to get new equipment', False, 'aquamarine4')
            equip_txt_rect = equip_txt_surf.get_rect(topleft=(710, 210))
            self.display_surface.blit(equip_txt_surf, equip_txt_rect)

        elif not available_tools.is_empty():
            tool = self.player.available_tools.peek()
            if not self.player.possessed_tools.is_here(tool):
                equip_txt_surf = self.font_small.render('Here is your newest equipment!', False, 'aquamarine4')
                equip_txt_rect = equip_txt_surf.get_rect(topleft=(710, 210))
                self.display_surface.blit(equip_txt_surf, equip_txt_rect)

                if tool == 'glass':
                    strg = 'magnifying glass'

                elif tool == 'binoculars':
                    strg = 'binoculars'
                
                surf = self.font_smaller.render(strg, False, 'Black')
                rect = surf.get_rect(center = box1.center) 
                self.display_surface.blit(surf, rect)
                if box1.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display_surface, 'black', box1, width = 4, border_radius=10)
                    self.selected_tool = tool 

            else:
                equip_txt_surf = self.font_small.render('You have acquired a new equipment!', False, 'aquamarine4')
                equip_txt_rect = equip_txt_surf.get_rect(topleft=(710, 210))
                self.display_surface.blit(equip_txt_surf, equip_txt_rect)

                if tool == 'glass':
                    strg = 'magnifying glass'

                elif tool == 'binoculars':
                    strg = 'binoculars'
                
                surf = self.font_smaller.render(strg, False, 'azure4')
                rect = surf.get_rect(center = box1.center) 
                self.display_surface.blit(surf, rect)
                if box1.collidepoint(pygame.mouse.get_pos()):
                    pygame.draw.rect(self.display_surface, 'azure4', box1, width = 4, border_radius=10)

                
=======

    def display_board(self):
        print('hello')
        #text
        explanation_text_surf = self.font_small.render(' Press ENTER to start a new day ', False, 'Black')
        explanation_text_rect = explanation_text_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', explanation_text_rect)
        self.display_surface.blit(explanation_text_surf, explanation_text_rect)
>>>>>>> b714464edd93ff01282798143cc34c210bb49cbf
