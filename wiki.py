import pygame 
from settings import *

class Wiki(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.display_surface = pygame.display.get_surface()
        self.imports()
        self.in_menu = False

    def imports(self):
        self.font_big = pygame.font.Font('../font/LycheeSoda.ttf', 50)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 30)

    def format_species_name_string(self, strg):
        res =''
        for char in strg:
            if char == '_':
                res+=' '
            else:
                res+= char
        return(res)

    def display_wiki(self, species):
        if self.in_menu:
            #pygame.draw.rect(self.display_surface, 'White', pygame.Rect(40,40,1200,640))

            #TEXT
            exit_txt_surf = self.font_smaller.render('  Press ESC to return to the dictionary ', False, 'Black')
            exit_txt_rect = exit_txt_surf.get_rect(center = (640, 665))

            #IMAGE
            full_path = '../graphics/wiki/'+species+'.png'
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_rect = image_surf.get_rect(center = (640, 360))

            #DISPLAY
            self.display_surface.blit(image_surf, image_rect)
            pygame.draw.rect(self.display_surface, 'Grey', exit_txt_rect, border_top_left_radius=10, border_top_right_radius=10)
            self.display_surface.blit(exit_txt_surf, exit_txt_rect)

            #OUT
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                self.in_menu = False


