import pygame
from settings import *

class Toggle:
    def __init__(self):
        #general setup
        self.display_surface = pygame.display.get_surface()
        self.font_small = pygame.font.Font('../font/LycheeSoda.ttf', 30)
        self.font_smaller = pygame.font.Font('../font/LycheeSoda.ttf', 20)
        self.current_slide = 0
        self.in_menu = False

        self.available_species_list= []        

        self.width = 400
        self.space = 10 
        self.padding = 8 

    def display_menu(self, known_species, well_known_species):
        if self.in_menu:
            if not known_species.is_empty():
                selected_species = self.selected_species(known_species)
                self.display_slide(self.current_slide, known_species, well_known_species)
                self.display_menu_info()

                well_known_L = well_known_species.convert_list()
                known_L = known_species.convert_list()

                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.Rect(650, 590, 50, 50).collidepoint(mouse_pos):
                            self.current_slide += 1 
                            self.display_slide(self.current_slide, known_species, well_known_species)
                            
                        if pygame.Rect(570, 590, 50, 50).collidepoint(mouse_pos):
                            self.current_slide -= 1
                            self.display_slide(self.current_slide, known_species, well_known_species)

                        if selected_species != False: #if player is hovering a species
                            if selected_species in known_L: #if known
                                if not selected_species in well_known_L: #not well known
                                    well_known_species.push(selected_species)

    def display_menu_info(self):
        #text
        welcome_txt_surf = self.font_small.render(' > Do you want more information on a specific species ? ', False, 'Black')
        welcome_txt_rect = welcome_txt_surf.get_rect(center = (640, 200))
        exit_txt_surf = self.font_smaller.render('  Press ESC to exit  ', False, 'Grey')
        exit_txt_rect = exit_txt_surf.get_rect(center = (640, 260))

        #display
        pygame.draw.rect(self.display_surface, 'White', welcome_txt_rect, border_radius=5)
        pygame.draw.rect(self.display_surface, 'White', exit_txt_rect, border_radius=3)
        self.display_surface.blit(welcome_txt_surf, welcome_txt_rect)
        self.display_surface.blit(exit_txt_surf, exit_txt_rect)

    def selected_species(self, known_species):
        #returns the known species that the player's mouse is hovering

        known_split = known_species.partition(6)
        known_list = known_species.convert_list()        

        possible_rect_slide = []
        for species in range(len(known_split[self.current_slide])):
            height_i = 300 + species*(self.padding + 30)
            possible_rect_slide.append((440, height_i, self.width, 30))
        
        mouse_pos = pygame.mouse.get_pos()
        found_it = False

        i = 0
        for possible_rect in possible_rect_slide:
            if pygame.Rect(possible_rect).collidepoint(mouse_pos):
                index = self.current_slide*6 + i 
                found_it = index+1
            i+=1
        
        if found_it == False:
            return False
        else:
            return known_list[index]

    def display_slide(self, current_slide, known_species, well_known_species):
        split_copy = known_species.partition(6)
        slide_index = [current_slide for current_slide in range(0, len(split_copy))]

        i = 0
        for species in split_copy[current_slide]:
            height_i = 300 + i*(self.padding + 30)
            if well_known_species.is_here(species):
                txt_surf = self.font_smaller.render(FORMAT(species), False, 'chartreuse3')
            else:
                txt_surf = self.font_smaller.render(FORMAT(species), False, 'Black')
            txt_rect = txt_surf.get_rect(center = pygame.Rect(440, height_i, self.width, 30).center)

            #background box
            pygame.draw.rect(self.display_surface, 'White', pygame.Rect(440, height_i, self.width, 30), border_radius=5)
                       
            #hover animation for box
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(440, height_i, self.width, 30).collidepoint(mouse_pos):
                if well_known_species.is_here(species):
                    pygame.draw.rect(self.display_surface, 'chartreuse3', pygame.Rect(440, height_i, self.width, 30), width = 3, border_radius=5)
                else:    
                    pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(440, height_i, self.width, 30), width = 3, border_radius=5)

            #display
            self.display_surface.blit(txt_surf, txt_rect)

            i += 1

        #next slide arrow button
        if not current_slide == slide_index[-1]: #if we're not on the last slide
            pygame.draw.rect(self.display_surface, 'White', pygame.Rect(680, 620, 20, 20), border_radius = 10)
            right_arrow_surf = self.font_small.render(' > ', False, 'Black')
            right_arrow_rect = right_arrow_surf.get_rect(center = (690, 630))
            self.display_surface.blit(right_arrow_surf, right_arrow_rect)

        #hover animation for the next slide button
        if not current_slide == slide_index[-1]: #if we're not on the last slide
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(650, 590, 50, 50).collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(680, 620, 20, 20), border_radius = 15)
                right_arrow_surf = self.font_small.render(' > ', False, 'White')
                right_arrow_rect =right_arrow_surf.get_rect(center = (690, 630))
                self.display_surface.blit(right_arrow_surf, right_arrow_rect)

        #previous slide arrow button
        if not current_slide == slide_index[0]: #if we're not on the first slide
            pygame.draw.rect(self.display_surface, 'White', pygame.Rect(600, 620, 20, 20), border_radius = 10)
            left_arrow_surf = self.font_small.render(' < ', False, 'Black')
            left_arrow_rect = left_arrow_surf.get_rect(center = (610, 630))
            self.display_surface.blit(left_arrow_surf, left_arrow_rect)

        #hover animation for the previous slide button
        if not current_slide == slide_index[0]: #if we're not on the first slide
            mouse_pos = pygame.mouse.get_pos()
            if pygame.Rect(570, 590, 50, 50).collidepoint(mouse_pos):
                pygame.draw.rect(self.display_surface, 'Black', pygame.Rect(600, 620, 20, 20), border_radius = 15)
                left_arrow_surf = self.font_small.render(' < ', False, 'White')
                left_arrow_rect = left_arrow_surf.get_rect(center = (610, 630))
                self.display_surface.blit(left_arrow_surf, left_arrow_rect)

        slide_nb_surf = self.font_smaller.render('  You are on slide number ' + str(current_slide+1) + '/'+ str(slide_index[-1]+1)+'  ', False, 'Grey')
        slide_nb_rect = slide_nb_surf.get_rect(center = (640, 570))

        pygame.draw.rect(self.display_surface, 'White', slide_nb_rect, border_radius=3)
        self.display_surface.blit(slide_nb_surf, slide_nb_rect)


