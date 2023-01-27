import sys
import pygame
from settings import *
from intromenu import Intromenu

class Action(pygame.sprite.Sprite):
    def __init__(self, first_encounter = True):
        self.display_surface = pygame.display.get_surface()

        self.first_encounter = first_encounter

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller =pygame.font.Font('../font/LycheeSoda.ttf', 15)

    def display_board_message(self):
        #text
        explanation_text_surf = self.font_small.render(' Press ENTER to start a new day ', False, 'Black')
        explanation_text_rect = explanation_text_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', explanation_text_rect)
        self.display_surface.blit(explanation_text_surf, explanation_text_rect)

    def display_small_tree(self):
        if self.first_encounter:
            #text
            new_species_strg = 'Congratulations! You have found a small tree'
            new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
            new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

            #display
            pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
            self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_large_tree(self):
        #text
        new_species_strg = 'Congratulations! You have found a large tree'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_bush(self):
        #text
        new_species_strg = 'Congratulations! You have found a bush'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_sunflower(self):
        #text
        new_species_strg = 'Congratulations! You have found a sunflower'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_pink_flower(self):
        #text
        new_species_strg = 'Congratulations! You have found a pink flower'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)
    
    def display_blue_flower(self):
        #text
        new_species_strg = 'Congratulations! You have found a blue flower'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_one_purple_mushroom(self):
        #text
        new_species_strg = 'Congratulations! You have found a purple mushroom'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_one_red_mushroom(self):
        #text
        new_species_strg = 'Congratulations! You have found a red mushroom'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_two_purple_mushrooms(self):
        #text
        new_species_strg = 'Congratulations! You have found a pair of purple mushrooms'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_two_red_mushrooms(self):
        #text
        new_species_strg = 'Congratulations! You have found a pair of red mushrooms'
        new_species_txt_surf = self.font_small.render(new_species_strg, False, 'Black')
        new_species_txt_rect = new_species_txt_surf.get_rect(topleft = (30, 35))

        #display
        pygame.draw.rect(self.display_surface, 'White', new_species_txt_rect)
        self.display_surface.blit(new_species_txt_surf, new_species_txt_rect)

    def display_message_bio(self):
        #text overlay
        strg_list = ['Congratulations! You have found a wild biologist !',
                    'You can ask them questions about a species you have discovered',
                    'To do so press the ENTER key']
        for strg in strg_list:
            txt_surf = self.font_small.render(strg, False, 'Black')
            txt_rect = txt_surf.get_rect(topleft = (30, 35+30*strg_list.index(strg)))

            #display
            pygame.draw.rect(self.display_surface, 'White', txt_rect)
            self.display_surface.blit(txt_surf, txt_rect)

    def display_warning(self):
        warning1_txt_surf = self.font_small.render(' Are you sure you want to return to the homescreen ? ', False, 'Black')
        warning1_txt_rect = warning1_txt_surf.get_rect(center = (640, 300))

        #button
        yes_surf = self.font_small.render('  yes I am sure  ', False, 'White')
        yes_rect = yes_surf.get_rect(center = (640, 370))                

        #hover animation more info button
        mouse_pos = pygame.mouse.get_pos()

        #display
        pygame.draw.rect(self.display_surface, 'White', pygame.Rect(200, 200, 880, 300), border_radius = 5)
        pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(210, 210, 860, 280), width=5,  border_radius = 5) #border
        pygame.draw.rect(self.display_surface, 'Black', yes_rect, border_radius=10)
        
        #hover animation more info button
        mouse_pos = pygame.mouse.get_pos()
        if yes_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.display_surface, 'chartreuse3', yes_rect, border_radius=10)
            yes_surf = self.font_small.render('  yes I am sure  ', False, 'White')
            yes_rect = yes_surf.get_rect(center = (640, 370))
            
        self.display_surface.blit(warning1_txt_surf, warning1_txt_rect)
        self.display_surface.blit(yes_surf, yes_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if yes_rect.collidepoint(mouse_pos):
                    intromenu = Intromenu()
                    intromenu.run()