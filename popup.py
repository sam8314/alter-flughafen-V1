import pygame
from settings import *

class PopUp(pygame.sprite.Sprite):
    def __init__(self, species, first_encounter = True):
        self.display_surface = pygame.display.get_surface()

        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 70)
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 15)

        self.species = FORMAT(species)
        self.first_encounter = first_encounter

        #text
        self.new_species_strg = '  Congratulations! You have found a '+self.species
        self.new_species_txt_surf = self.font_small.render(self.new_species_strg, False, 'Black')
        self.new_species_txt_rect = self.new_species_txt_surf.get_rect(midtop = (640, 0))

    def display(self):
        #display
        if self.first_encounter :
            pygame.draw.rect(self.display_surface, 'White', self.new_species_txt_rect, border_bottom_left_radius=10, border_bottom_right_radius=10)
            self.display_surface.blit(self.new_species_txt_surf, self.new_species_txt_rect)
